"""The UNVIBECODE.md map file: build, render, parse, compare.

Design rules (each one comes from the 13 Nov 2026 trial, see /evidence/README.md):
* Key connections by (source file, target file, symbol) and never by line number or chunk id.
  Chunk ids changed for 97 of 481 sections after a 19-line edit, while the
  (file, file, symbol) set did not change at all.
* Never write timestamps, job ids or commit hashes into the file, so an unchanged
  structure renders to byte-identical text and git shows no diff.
* Show suspicious connections and coverage gaps openly instead of hiding them in a graph.
"""
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import PurePosixPath

FORMAT = "unvibecode-map:v1"
FILENAME = "UNVIBECODE.md"
HUB_MIN_IMPORTERS = 10


@dataclass
class CodeMap:
    repository: str
    edges: dict                       # (source, target) -> sorted tuple of symbols ('' excluded)
    source_files: int = 0
    files: list = field(default_factory=list)
    unresolved_relative_imports: int = 0
    workflows: list = field(default_factory=list)   # workflows.Workflow, from the Business Workflow Map

    # ---- derived views -------------------------------------------------
    def importers(self):
        """target file -> set of files that directly connect to it."""
        result = defaultdict(set)
        for (src, dst) in self.edges:
            result[dst].add(src)
        return result

    def edge_keys(self):
        """Flat set of (source, target, symbol); symbol '' means a file-level connection."""
        keys = set()
        for (src, dst), symbols in self.edges.items():
            keys.add((src, dst, ""))
            keys.update((src, dst, s) for s in symbols)
        return keys


def from_bundle(bundle):
    edges = defaultdict(set)
    for c in bundle.connections:
        src, dst = c.get("source_file"), c.get("target_file")
        if not src or not dst or src == dst:
            continue
        edges[(src, dst)]  # file-level connection exists even without a symbol
        if c.get("symbol"):
            edges[(src, dst)].add(c["symbol"])
    relative = {(u.get("source_file") or u.get("source"), u.get("line"), u.get("module"))
                for u in bundle.unresolved if str(u.get("module") or "").startswith(".")}
    return CodeMap(
        repository=bundle.repository,
        edges={k: tuple(sorted(v)) for k, v in edges.items()},
        source_files=int(bundle.manifest.get("source_files") or len(bundle.files)),
        files=list(bundle.files),
        unresolved_relative_imports=len(relative),
    )


# ---- suspicious connections ---------------------------------------------
def _is_test_path(path):
    p = PurePosixPath(path)
    return (any(part in {"tests", "test", "__tests__", "spec"} for part in p.parts[:-1])
            or p.name.startswith("test_") or p.name == "conftest.py"
            or re.search(r"[._](test|spec)\.[jt]sx?$", p.name) is not None)


def suspicious(code_map):
    """Return [(kind, text, sort_key)] for connections a reviewer should double-check."""
    findings = []
    for (src, dst), symbols in sorted(code_map.edges.items()):
        if _is_test_path(dst) and not _is_test_path(src):
            sym = f" · {', '.join(symbols)}" if symbols else ""
            findings.append(("test-target", f"`{src}` → `{dst}`{sym} — non-test code connected into test code"))
    packages = {PurePosixPath(f).parent.name for f in code_map.files
                if PurePosixPath(f).name == "__init__.py"}
    importers = code_map.importers()
    for dst in sorted(importers):
        stem = PurePosixPath(dst).stem
        if PurePosixPath(dst).suffix == ".py" and stem in packages and PurePosixPath(dst).name != "__init__.py":
            findings.append(("shadowing", f"{len(importers[dst])} files → `{dst}` — its name shadows "
                                          f"the package `{stem}/`; imports of `{stem}` may be mis-resolved"))
    return findings


def area(path):
    parts = PurePosixPath(path).parts
    if len(parts) <= 1:
        return "(root)"
    if parts[0] in {"src", "packages", "services", "apps", "libs", "lib", "cmd", "internal"} and len(parts) > 2:
        return "/".join(parts[:2])
    return parts[0]


# ---- render ---------------------------------------------------------------
def render(code_map, top=15):
    imp = code_map.importers()
    lines = [
        f"# UnvibeCode Map: {code_map.repository}",
        "",
        "> The [UnvibeCode](https://github.com/FinanceFlash/unvibecode) Business Workflow Map and Connected Code Map "
        "for this repository, kept as text so git can diff it and every clone carries it.",
        "> What does my change touch? `unvibe` · Refresh: `unvibecode-mapfile build` · "
        "Check a pull request: `unvibecode-mapfile check`",
        "> Written by unvibecode-mapfile (community prototype, not an official UnvibeCode product). "
        "Do not edit by hand.",
        "",
        f"<!-- {FORMAT} source_files={code_map.source_files} connected_files={len({f for e in code_map.edges for f in e})} "
        f"connections={len(code_map.edges)} unresolved_relative_imports={code_map.unresolved_relative_imports} -->",
        "",
    ]
    lines += render_workflows(code_map.workflows)
    lines += [
        "## Most-imported files",
        "",
        "Change these with care: many files connect to them directly.",
        "",
        "| File | Direct importers |",
        "|---|---:|",
    ]
    ranked = sorted(imp.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:top]
    lines += [f"| `{f}` | {len(s)} |" for f, s in ranked]
    area_pairs = Counter((area(s), area(d)) for (s, d) in code_map.edges if area(s) != area(d))
    lines += ["", "## Area connections", "", "| From | To | Connections |", "|---|---|---:|"]
    lines += [f"| `{a}` | `{b}` | {n} |" for (a, b), n in sorted(area_pairs.items(), key=lambda kv: (-kv[1], kv[0]))]
    if not area_pairs:
        lines += ["| (none) | every recorded connection stays inside one area | 0 |"]
    flagged = suspicious(code_map)
    lines += ["", "## Check these connections", ""]
    if flagged:
        lines += ["These look wrong or surprising. Verify them; if UnvibeCode is wrong, report it upstream.", ""]
        lines += [f"- {text}" for _, text in flagged]
    else:
        lines += ["None found."]
    lines += ["", "## Coverage", "",
              f"- Source files analysed: {code_map.source_files}",
              f"- Files with at least one connection: {len({f for e in code_map.edges for f in e})}"
              + (f" ({100 * len({f for e in code_map.edges for f in e}) // code_map.source_files}%)" if code_map.source_files else ""),
              f"- Relative imports UnvibeCode could not resolve: {code_map.unresolved_relative_imports}"]
    if code_map.source_files and len(code_map.edges) < code_map.source_files / 10:
        lines.append("- **Sparse map:** fewer connections than one per ten files. Reach and deltas below "
                     "will miss real dependencies for this repository.")
    lines += ["", "## Connections", "",
              "One line per connected file pair, with the symbols used. Line numbers are left out on purpose, "
              "so this section only changes when structure changes.", ""]
    by_source = defaultdict(list)
    for (src, dst), symbols in code_map.edges.items():
        by_source[src].append((dst, symbols))
    for src in sorted(by_source):
        lines.append(f"### `{src}`")
        for dst, symbols in sorted(by_source[src]):
            lines.append(f"- → `{dst}`" + (f" · {', '.join(symbols)}" if symbols else ""))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_workflows(workflows):
    out = ["## Business workflows", ""]
    if not workflows:
        return out + ["Not available yet: UnvibeCode's business analysis has not produced a workflow map for "
                      "this repository. The sections below still work.", ""]
    out += [f"{len(workflows)} workflows from the UnvibeCode Business Workflow Map. "
            "Refreshed on purpose (weekly or per release), not on every change. Line numbers are left out "
            "so later commits do not invalidate it.", ""]
    for w in workflows:
        out += [f"### Workflow · {w.title}", f"Area: {w.area}", ""]
        out += [f"- `{f}` · {', '.join(syms)}" if syms else f"- `{f}`" for f, syms in w.refs.items()]
        out.append("")
    return out


# ---- parse ----------------------------------------------------------------
_HEADER = re.compile(r"^# UnvibeCode Map: (.+)$")
_META = re.compile(r"<!-- unvibecode-map:v1 (.*?) -->")
_SOURCE = re.compile(r"^### `(.+)`$")
_EDGE = re.compile(r"^- → `(.+?)`(?: · (.+))?$")
_WF_TITLE = re.compile(r"^### Workflow · (.+)$")
_WF_AREA = re.compile(r"^Area: (.+)$")
_WF_REF = re.compile(r"^- `(.+?)`(?: · (.+))?$")


def parse(text):
    from .workflows import Workflow
    repo, meta, edges, current, in_connections = "repository", {}, {}, None, False
    section, workflows = "", []
    for line in text.splitlines():
        if line.startswith("## "):
            section = line.strip()
        if section == "## Business workflows":
            if (m := _WF_TITLE.match(line)):
                workflows.append(Workflow(title=m.group(1), area=""))
            elif workflows and (m := _WF_AREA.match(line)):
                workflows[-1].area = m.group(1)
            elif workflows and (m := _WF_REF.match(line)):
                workflows[-1].refs[m.group(1)] = tuple(x.strip() for x in m.group(2).split(",")) if m.group(2) else ()
            continue
        if (m := _HEADER.match(line)):
            repo = m.group(1)
        elif (m := _META.search(line)):
            meta = dict(kv.split("=", 1) for kv in m.group(1).split())
        elif line.startswith("## "):
            in_connections = line.strip() == "## Connections"
        elif in_connections and (m := _SOURCE.match(line)):
            current = m.group(1)
        elif in_connections and current and (m := _EDGE.match(line)):
            symbols = tuple(s.strip() for s in m.group(2).split(",")) if m.group(2) else ()
            edges[(current, m.group(1))] = symbols
    if not meta:
        raise ValueError("Not an UnvibeCode map file (missing unvibecode-map:v1 marker)")
    return CodeMap(repository=repo, edges=edges, source_files=int(meta.get("source_files", 0)),
                   unresolved_relative_imports=int(meta.get("unresolved_relative_imports", 0)),
                   workflows=workflows)


# ---- delta (freeze semantics) -----------------------------------------------
def delta(old, new):
    """Connections added and removed, keyed without line numbers (ArchUnit-freeze style)."""
    a, b = old.edge_keys(), new.edge_keys()
    # Report symbol-level changes; report a bare file pair only when the pair itself appears/disappears.
    def visible(keys, other_pairs):
        with_symbols = {(k[0], k[1]) for k in keys if k[2]}
        return sorted(k for k in keys
                      if k[2] or ((k[0], k[1]) not in other_pairs and (k[0], k[1]) not in with_symbols))
    added, removed = b - a, a - b
    return visible(added, set(old.edges)), visible(removed, set(new.edges))


def render_delta(added, removed, markdown=False):
    def fmt(k):
        return f"`{k[0]}` → `{k[1]}`" + (f" · {k[2]}" if k[2] else "")
    if not added and not removed:
        return "No structural change: connections match UNVIBECODE.md."
    out = [f"Structural change: +{len(added)} / -{len(removed)} connections versus UNVIBECODE.md"]
    out += [("- **added** " if markdown else "  + ") + fmt(k) for k in added]
    out += [("- **removed** " if markdown else "  - ") + fmt(k) for k in removed]
    return "\n".join(out)
