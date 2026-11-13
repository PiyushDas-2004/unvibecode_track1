"""unvibecode-mapfile: keep the UnvibeCode Connected Code Map as UNVIBECODE.md in the repository.

Commands
  build   run UnvibeCode once (or read a bundle) and write UNVIBECODE.md
  check   compare current structure with the committed UNVIBECODE.md (freeze semantics)
  impact  reach of a change, from UNVIBECODE.md + git diff; never uploads
  diff    structural difference between two map files or two git revisions of one
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from . import __version__
from . import changes
from . import impact as impact_mod
from .bundle import load_bundle, run_unvibecode
from .mapfile import FILENAME, delta, from_bundle, parse, render, render_delta
from .workflows import parse_workflow_html, touched_workflows


def log_usage(event, **fields):
    """Opt-in, local-only usage log. Nothing is sent anywhere.

    Enabled only when UNVIBECODE_MAPFILE_USAGE_LOG is set to a file path. Records the event name,
    a timestamp and whether it ran in CI (the CI env var), which separates automated from manual use.
    """
    path = os.environ.get("UNVIBECODE_MAPFILE_USAGE_LOG")
    if not path:
        return
    record = {"event": event, "ts": int(time.time()), "trigger": "ci" if os.environ.get("CI") else "manual",
              "version": __version__, **fields}
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")


_TEMP_RESULTS = []


def _current_map(args):
    bundle = args.bundle
    if not bundle:
        bundle = run_unvibecode(args.repository)
        _TEMP_RESULTS.append(Path(bundle).parent.parent)   # the temporary --output folder
    code_map = from_bundle(load_bundle(bundle))
    code_map.bundle_path = Path(bundle)
    return code_map


def _cleanup():
    """UnvibeCode results contain source excerpts; do not leave them in the temp directory."""
    while _TEMP_RESULTS:
        shutil.rmtree(_TEMP_RESULTS.pop(), ignore_errors=True)


def _workflow_source(args, code_map):
    """Business Workflow Map page: --workflows, else the one UnvibeCode wrote next to the bundle."""
    if getattr(args, "workflows", None):
        return Path(args.workflows)
    folder = Path(code_map.bundle_path)
    folder = folder if folder.is_dir() else folder.parent
    for candidate in (folder / "report-support" / "business-workflows.html", folder / "business-workflows.html"):
        if candidate.exists():
            return candidate
    return None


def _map_path(args):
    return Path(args.map) if args.map else Path(args.repository) / FILENAME


def cmd_build(args):
    code_map = _current_map(args)
    target = _map_path(args)
    source = _workflow_source(args, code_map)
    if source:
        code_map.workflows = parse_workflow_html(source.read_text(encoding="utf-8"))
        print(f"Business Workflow Map: {len(code_map.workflows)} workflows from {source.name}.")
    elif target.exists():
        # Business analysis unavailable this run (e.g. the hosted LLM stage is out of credits):
        # keep the previous workflow index instead of erasing it.
        code_map.workflows = parse(target.read_text(encoding="utf-8")).workflows
        if code_map.workflows:
            print(f"Business analysis unavailable this run; kept {len(code_map.workflows)} workflows from {target.name}.")
    text = render(code_map)
    changed = not target.exists() or target.read_text(encoding="utf-8") != text
    target.write_text(text, encoding="utf-8")
    print(f"{'Wrote' if changed else 'Unchanged'} {target}: {len(code_map.edges)} connections, "
          f"{code_map.source_files} source files.")
    log_usage("build", changed=changed, connections=len(code_map.edges), workflows=len(code_map.workflows))
    return 0


def cmd_check(args):
    committed_path = _map_path(args)
    if not committed_path.exists():
        print(f"No {committed_path} yet. Run `unvibecode-mapfile build` and commit it.")
        return 1 if args.strict else 0
    committed = parse(committed_path.read_text(encoding="utf-8"))
    if args.since and not args.bundle:
        lines = impact_mod.changed_lines(args.repository, args.since, args.head)
        gated = impact_mod.import_changes(lines)
        if not gated:
            print("No import lines changed since " + args.since + ": skipped the UnvibeCode upload; "
                  "UNVIBECODE.md is still valid.")
            log_usage("check", uploaded=False, added=0, removed=0)
            return 0
    current = _current_map(args)
    added, removed = delta(committed, current)
    print(render_delta(added, removed, markdown=args.markdown))
    if added or removed:
        print("Refresh with `unvibecode-mapfile build` and commit UNVIBECODE.md with this change.")
    log_usage("check", uploaded=not args.bundle, added=len(added), removed=len(removed))
    return 1 if (args.strict and (added or removed)) else 0


def cmd_impact(args):
    map_path = _map_path(args)
    code_map = parse(map_path.read_text(encoding="utf-8"))
    files = impact_mod.changed_files(args.repository, args.base, args.head)
    hunks = changes.diff_hunks(args.repository, args.base, args.head)
    lines = changes.flat_lines(hunks)
    names = changes.changed_definitions(args.repository, hunks, args.base, args.head)
    report = impact_mod.reach(code_map, files, lines, names)
    hits = touched_workflows(code_map.workflows, files, names)
    print(impact_mod.render(report, impact_mod.import_changes(lines), hits, bool(code_map.workflows),
                            markdown=args.markdown, oneline=args.oneline))
    log_usage("impact", changed_files=len(files), hub=any(r.hub for r in report), workflows_touched=len(hits),
              entry=getattr(args, "entry", "impact"))
    return 0


def _load_map_arg(value, repository):
    """A path to a map file, or REV:PATH / REV (git revision of UNVIBECODE.md)."""
    p = Path(value)
    if p.exists():
        return parse(p.read_text(encoding="utf-8"))
    spec = value if ":" in value else f"{value}:{FILENAME}"
    text = subprocess.run(["git", "-C", repository, "show", spec], capture_output=True, text=True, check=True).stdout
    return parse(text)


def cmd_diff(args):
    added, removed = delta(_load_map_arg(args.old, args.repository), _load_map_arg(args.new, args.repository))
    print(render_delta(added, removed, markdown=args.markdown))
    log_usage("diff", added=len(added), removed=len(removed))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="unvibecode-mapfile", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p, bundle=True):
        p.add_argument("--repository", default=".", help="repository root (default: current directory)")
        p.add_argument("--map", help=f"map file path (default: <repository>/{FILENAME})")
        if bundle:
            p.add_argument("--bundle", help="use an existing *-repository-context.zip instead of running UnvibeCode")
        p.add_argument("--markdown", action="store_true", help="Markdown output for PR descriptions / CI summaries")

    p = sub.add_parser("build", help="write UNVIBECODE.md"); common(p)
    p.add_argument("--workflows", help="business-workflows.html from an UnvibeCode results folder "
                                        "(default: found next to the bundle; else kept from the existing map)")
    p.set_defaults(func=cmd_build)
    p = sub.add_parser("check", help="report connections added/removed versus UNVIBECODE.md"); common(p)
    p.add_argument("--since", help="git ref; skip the upload when no import line changed since it")
    p.add_argument("--head", help="git ref for the end of the range (default: working tree)")
    p.add_argument("--strict", action="store_true", help="exit 1 when structure changed (default: warn only)")
    p.set_defaults(func=cmd_check)
    p = sub.add_parser("impact", help="reach of a change; local only"); common(p, bundle=False)
    p.add_argument("--base", default="HEAD", help="git ref to compare with (default: HEAD)")
    p.add_argument("--head", help="git ref for the end of the range (default: working tree)")
    p.add_argument("--oneline", action="store_true", help="one line, e.g. for a PR check-run title")
    p.set_defaults(func=cmd_impact)
    p = sub.add_parser("diff", help="compare two map files or git revisions"); common(p, bundle=False)
    p.add_argument("old"); p.add_argument("new"); p.set_defaults(func=cmd_diff)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"[unvibecode-mapfile] {exc}", file=sys.stderr)
        return 2
    finally:
        _cleanup()


def unvibe(argv=None):
    """`unvibe`: the deliberate, typed entry point. Same as `impact` on the working tree."""
    argv = list(sys.argv[1:] if argv is None else argv)
    if any(a in {"-h", "--help"} for a in argv):
        print("usage: unvibe [--base REF] [--head REF] [--markdown] [--oneline] [--repository DIR]\n\n"
              "What did my change (or the AI's change) touch? Business workflows first, then code reach.\n"
              "Reads UNVIBECODE.md and git diff only: no upload, no LLM. Community prototype.")
        return 0
    return main(["impact", *argv])


if __name__ == "__main__":
    sys.exit(main())
