"""Reach of a change, computed locally from UNVIBECODE.md and `git diff` (no upload, no LLM)."""
import re
import subprocess
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass

from . import changes
from .mapfile import FILENAME, HUB_MIN_IMPORTERS

# Lines that can change cross-file structure. Deliberately broad: a false "yes" only costs one
# refresh; a false "no" would leave the map stale. Languages follow UnvibeCode's README table.
IMPORT_LINE = re.compile(
    r"^\s*(from\s+\S+\s+import\b|import\s+\S|export\s.*\bfrom\s|.*\brequire(_once)?\s*\(|"
    r"use\s+[\w\\:]+|require\s+['\"]|include(_once)?\s*\(?['\"]|\"[\w./-]+\"\s*$|\w+\s+\"[\w./-]+\"\s*$)")


def _git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout


def _range(base, head):
    return [f"{base}...{head}"] if head else [base]


def changed_files(repo, base="HEAD", head=None, include_untracked=True):
    files = set(_git(repo, "diff", "--name-only", *_range(base, head)).split("\n"))
    if include_untracked and not head:
        files |= set(_git(repo, "ls-files", "--others", "--exclude-standard").split("\n"))
    return sorted(f for f in files if f and Path(f).name != FILENAME)   # the map itself is not "your change"


def changed_lines(repo, base="HEAD", head=None):
    """file -> list of changed line texts (added and removed) plus hunk-header context."""
    return changes.flat_lines(changes.diff_hunks(repo, base, head))


SOURCE_SUFFIXES = {".py", ".pyi", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".go", ".rs", ".php", ".rb"}


def import_changes(lines_by_file):
    """Source files (not docs) whose added/removed lines include an import-like line."""
    return sorted(f for f, lines in lines_by_file.items()
                  if Path(f).suffix.lower() in SOURCE_SUFFIXES and any(IMPORT_LINE.match(l) for l in lines))


def _definition_pattern(symbol):
    """A change counts as touching `symbol` when it is inside or at its definition:
    git's hunk header names the enclosing def/class/func, and a changed line may be the definition itself."""
    s = re.escape(symbol)
    return re.compile(rf"(\b(def|class|func|function|const|let|var|type|struct|fn)\s+(\([^)]*\)\s*)?{s}\b|^\s*{s}\s*[:=])")


@dataclass
class FileReach:
    path: str
    importers: dict          # importer -> symbols it uses from this file
    touched_symbols: dict    # symbol -> importers that use it (symbols appearing in changed lines)

    @property
    def hub(self):
        return len(self.importers) >= HUB_MIN_IMPORTERS


def reach(code_map, files, lines_by_file, names_by_file=None):
    """names_by_file (from changes.changed_definitions) gives exact touched definitions; without it,
    fall back to matching definition patterns in the changed text."""
    users = defaultdict(dict)
    for (src, dst), symbols in code_map.edges.items():
        users[dst][src] = symbols
    report = []
    for f in files:
        imp = users.get(f, {})
        text = "\n".join(lines_by_file.get(f, []))
        touched = defaultdict(list)
        for importer, symbols in sorted(imp.items()):
            for s in symbols:
                hit = (changes.matches(s, names_by_file.get(f, set())) if names_by_file is not None
                       else any(_definition_pattern(s).search(line) for line in text.splitlines()))
                if hit:
                    touched[s].append(importer)
        report.append(FileReach(f, dict(sorted(imp.items())), dict(sorted(touched.items()))))
    return report


def _short(text, n=60):
    return text if len(text) <= n else text[:n - 1] + "…"


def render(report, import_files, workflow_hits=(), workflows_known=False, markdown=False, oneline=False, limit=8):
    total = len({i for r in report for i in r.importers})
    hubs = [r.path for r in report if r.hub]
    if oneline:
        if workflow_hits:
            biz = f"{len(workflow_hits)} business workflow(s): " + "; ".join(_short(w.title, 48) for w, _, _ in workflow_hits)
        else:
            biz = "no mapped business workflow" if workflows_known else "business map not available"
        state = "map may be stale" if import_files else "map current"
        return f"UnvibeCode · {biz} · {total} direct importer(s){' · hub touched' if hubs else ''} · {state}"

    out = []
    title = "UnvibeCode business reach"
    if workflow_hits:
        out.append(f"{'### ' if markdown else ''}{title}: this change touches {len(workflow_hits)} business workflow(s)")
        for wf, matches, strength in workflow_hits:
            where = "; ".join(
                (f"changed {', '.join(syms)} in {f}" if syms else f"same file {f}") for f, syms in matches)
            label = "" if strength == "symbol" else " (file shared, no referenced symbol changed)"
            out.append(f"{'- ' if markdown else '  '}{wf.title} [{wf.area}]{label}: {where}")
    else:
        out.append(f"{'### ' if markdown else ''}{title}: "
                   + ("no mapped business workflow touched." if workflows_known else
                      "business workflow map not available yet; showing code reach only."))

    connected = [r for r in report if r.importers]
    out.append(("**Code reach:** " if markdown else "Code reach: ")
               + f"{len(report)} changed file(s); {total} other file(s) import them directly"
               + (f"; hub touched" if hubs else "") + ".")
    for r in connected:
        tag = " [hub]" if r.hub else ""
        out.append(f"- `{r.path}`{tag}: {len(r.importers)} direct importer(s)" if markdown
                   else f"  {r.path}{tag}: {len(r.importers)} direct importer(s)")
        for sym, who in r.touched_symbols.items():
            names = ", ".join(f"`{w}`" if markdown else w for w in who[:limit]) + (" …" if len(who) > limit else "")
            out.append(f"  - changed symbol `{sym}` is used by {names}" if markdown
                       else f"      changed symbol {sym} is used by {names}")
    quiet = [r.path for r in report if not r.importers]
    if quiet:
        out.append(f"{'- ' if markdown else '  '}{len(quiet)} changed file(s) have no recorded importers.")
    if import_files:
        out.append(("**Import lines changed** in " if markdown else "Import lines changed in ")
                   + ", ".join(f"`{f}`" if markdown else f for f in import_files)
                   + ": structure may have changed; run `unvibecode-mapfile check`.")
    else:
        out.append("No import lines changed: UNVIBECODE.md stays valid; no upload needed.")
    if markdown:
        out.append("\n<sub>Computed locally from UNVIBECODE.md (UnvibeCode Business Workflow Map + Connected Code Map) "
                   "by unvibecode-mapfile, a community prototype. No code was uploaded for this report.</sub>")
    return "\n".join(out)
