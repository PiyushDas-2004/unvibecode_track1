"""Which definitions did a git change touch?

Python (UnvibeCode's best-covered language in the trial): exact enclosing `Class.method` for every
added or removed line, from indentation in the before/after file versions.
Other languages: names from git's hunk headers and from changed definition lines. A hunk header names
the definition *above* the first changed line, so it is ignored when that line is itself a definition
(this fixed a real false positive on django-payments d1eea51).
"""
import re
import subprocess
import tempfile
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

_DIFF_DRIVERS = "".join(f"*.{ext} diff={drv}\n" for ext, drv in [
    ("py", "python"), ("pyi", "python"), ("go", "golang"), ("rs", "rust"), ("php", "php"),
    ("rb", "ruby"), ("java", "java"), ("cs", "csharp"), ("kt", "kotlin")])
_HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(.*)$")
_DEF = re.compile(r"\b(?:def|class|func|function|fn|struct|type|interface|trait|module)\s+"
                  r"(?:\([^)]*\)\s*)?([A-Za-z_]\w*)")
_PY_DEF = re.compile(r"^(\s*)(?:async\s+def|def|class)\s+([A-Za-z_]\w*)")
_TOP_ASSIGN = re.compile(r"^([A-Za-z_]\w*)\s*(?::[^=]+)?=(?!=)")


@dataclass
class Hunk:
    old_start: int
    new_start: int
    header: str
    removed: list = field(default_factory=list)   # (old line number, text)
    added: list = field(default_factory=list)     # (new line number, text)


def _git(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=check).stdout


def diff_hunks(repo, base="HEAD", head=None):
    """file -> [Hunk] for `git diff base...head` (or base vs working tree)."""
    rng = [f"{base}...{head}"] if head else [base]
    with tempfile.NamedTemporaryFile("w", suffix=".gitattributes", delete=False) as fh:
        fh.write(_DIFF_DRIVERS)
    try:
        text = _git(repo, "-c", f"core.attributesFile={fh.name}", "diff", "-U0", "--no-color", *rng)
    finally:
        Path(fh.name).unlink(missing_ok=True)
    hunks, current, old_no, new_no = defaultdict(list), None, 0, 0
    for line in text.splitlines():
        if line.startswith("--- "):
            current = line[6:] if line.startswith("--- a/") else None
        elif line.startswith("+++ "):
            if line.startswith("+++ b/"):
                current = line[6:]
        elif current and (m := _HUNK.match(line)):
            old_no, new_no = int(m.group(1)), int(m.group(3))
            hunks[current].append(Hunk(old_no, new_no, m.group(5).strip()))
        elif current and hunks[current] and line[:1] == "-":
            hunks[current][-1].removed.append((old_no, line[1:])); old_no += 1
        elif current and hunks[current] and line[:1] == "+":
            hunks[current][-1].added.append((new_no, line[1:])); new_no += 1
    return dict(hunks)


def flat_lines(hunks_by_file):
    """file -> header + changed line texts (the format the rest of the tool already uses)."""
    return {f: [x for h in hs for x in ([h.header] + [t for _, t in h.removed] + [t for _, t in h.added])]
            for f, hs in hunks_by_file.items()}


def python_scopes(source):
    """Line number (1-based) -> qualified enclosing definition ('Class.method', or '' at module level).

    A non-blank code line closes every scope opened at the same or deeper indentation. Lines that
    start with a closing bracket (multi-line signatures/calls) and comments never close a scope."""
    scopes, stack = {}, []
    for no, line in enumerate(source.splitlines(), 1):
        stripped = line.strip()
        if stripped and not stripped.startswith(("#", ")", "]", "}")):
            indent = len(line) - len(line.lstrip())
            while stack and indent <= stack[-1][0]:
                stack.pop()
            if (m := _PY_DEF.match(line)):
                stack.append((len(m.group(1)), m.group(2)))
        scopes[no] = ".".join(name for _, name in stack)
    return scopes


def _file_at(repo, rev, path):
    if rev is None:
        p = Path(repo) / path
        return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""
    return _git(repo, "show", f"{rev}:{path}", check=False)


def changed_definitions(repo, hunks_by_file, base="HEAD", head=None):
    """file -> set of names touched. Python: qualified names ('BasePayment.save') plus their
    top-level component; other languages: plain names."""
    result = {}
    if head:  # `git diff base...head` compares against the merge base, so read the old side there too
        base = _git(repo, "merge-base", base, head).strip() or base
    for path, hunks in hunks_by_file.items():
        names = set()
        if path.endswith((".py", ".pyi")):
            old = python_scopes(_file_at(repo, base, path)) if any(h.removed for h in hunks) else {}
            new = python_scopes(_file_at(repo, head, path)) if any(h.added for h in hunks) else {}
            for h in hunks:
                for no, text in h.removed:
                    names.add(old.get(no, ""))
                    if (m := _TOP_ASSIGN.match(text)):
                        names.add(m.group(1))
                for no, text in h.added:
                    names.add(new.get(no, ""))
                    if (m := _TOP_ASSIGN.match(text)):
                        names.add(m.group(1))
        else:
            for h in hunks:
                changed = [t for _, t in h.removed] + [t for _, t in h.added]
                first_is_def = bool(changed) and bool(_DEF.search(changed[0]))
                sources = changed if first_is_def else [h.header] + changed
                names |= {m.group(1) for line in sources for m in _DEF.finditer(line)}
        names.discard("")
        result[path] = names
    return result


def matches(symbol, names):
    """Does a referenced symbol ('Class.method', 'Class', 'func') match the touched names?"""
    symbol = symbol.rstrip("()")
    if symbol in names:
        return True
    if any(n.startswith(symbol + ".") for n in names):          # change inside a referenced class
        return True
    qualified = [n for n in names if "." in n]
    if "." in symbol or qualified:                               # Python: require the exact qualified name
        return False
    return symbol.split(".")[-1] in names                        # other languages: plain name
