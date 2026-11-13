"""Read UnvibeCode's Complete Repository Context bundle, or produce one with the official CLI.

This module only *reads* the documented bundle files (manifest.json, connections.jsonl,
chunks.jsonl, unresolved_relationships.jsonl). It does not contain or copy any UnvibeCode
engine code. The adapter calls the public CLI exactly as a user would.
"""
import json
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Bundle:
    repository: str
    manifest: dict
    connections: list            # dicts from connections.jsonl
    files: list = field(default_factory=list)       # every source file the engine saw
    unresolved: list = field(default_factory=list)  # dicts from unresolved_relationships.jsonl


def _read_jsonl(text):
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def load_bundle(path):
    """Load a bundle from a *-repository-context.zip or from a directory with the same files."""
    path = Path(path)
    if path.is_dir():
        def read(name):
            p = path / name
            return p.read_text(encoding="utf-8") if p.exists() else ""
    elif zipfile.is_zipfile(path):
        archive = zipfile.ZipFile(path)
        names = set(archive.namelist())

        def read(name):
            return archive.read(name).decode("utf-8") if name in names else ""
    else:
        raise ValueError(f"Not a repository-context ZIP or directory: {path}")
    manifest_text = read("manifest.json")
    if not manifest_text:
        raise ValueError(f"{path} has no manifest.json; is this an UnvibeCode repository-context bundle?")
    manifest = json.loads(manifest_text)
    chunks = _read_jsonl(read("chunks.jsonl"))
    return Bundle(
        repository=manifest.get("repository", "repository"),
        manifest=manifest,
        connections=_read_jsonl(read("connections.jsonl")),
        files=sorted({c["file"] for c in chunks if c.get("file")}),
        unresolved=_read_jsonl(read("unresolved_relationships.jsonl")),
    )


def run_unvibecode(repository, python=sys.executable):
    """Run the official CLI once and return the path of the repository-context ZIP it produced.

    Output goes to a temporary folder, so nothing is written inside the analysed repository.
    The CLI exits with code 1 when the hosted business-analysis lane is partial (observed on
    every run on 13 Nov 2026) even though the deterministic Connected Code Map lane succeeded,
    so the exit code is not trusted; the presence of the bundle is.
    """
    out = Path(tempfile.mkdtemp(prefix="unvibecode-mapfile-"))
    proc = subprocess.run(
        [python, "-m", "unvibecode", "review", "--repository", str(repository),
         "--output", str(out), "--no-open-browser"],
        capture_output=True, text=True)
    found = sorted(out.rglob("*-repository-context.zip"))
    if not found:
        import shutil
        shutil.rmtree(out, ignore_errors=True)
        tail = "\n".join((proc.stdout + proc.stderr).splitlines()[-15:])
        raise RuntimeError("UnvibeCode did not produce a repository-context bundle.\n" + tail)
    return found[0]
