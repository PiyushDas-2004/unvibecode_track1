"""Re-run the whole UnvibeCode trial and the prototype demo on your own machine.

Usage (Windows, macOS or Linux; needs Python 3.11+, git and internet):
    python scripts/reproduce_trial.py

It creates a work folder OUTSIDE this repository (default: ~/unvibecode-trial) with a fresh virtual
environment and the analysed repositories, runs `python -m unvibecode review` on each pinned commit,
then runs the prototype tests and the django-payments `unvibe` demo. Logs and a SUMMARY.md are
written to evidence/rerun_<UTC date>/ with job IDs redacted (they are bearer tokens).
Every run uploads the repository's source files to the hosted UnvibeCode service, like the
official CLI always does; all repositories here are public.
"""
import datetime
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = Path(os.environ.get("UNVIBECODE_TRIAL_DIR", Path.home() / "unvibecode-trial"))
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d")
OUT = ROOT / "evidence" / f"rerun_{STAMP}"
JOB_ID = re.compile(r"\b[0-9a-f]{32}\b")

TARGETS = [  # name, url, commit (same commits as the original trial)
    ("flask", "https://github.com/pallets/flask", "49943b5a94413a530761350f04e896f76e8d620e"),
    ("node-express-realworld-example-app", "https://github.com/gothinkster/node-express-realworld-example-app",
     "30b68e1e881462b2f4164ea09ab4c4f5699c7b0b"),
    ("spring-petclinic", "https://github.com/spring-projects/spring-petclinic", "500158f732419217507c7656904b8e6aa1bcc0d6"),
    ("microservices-demo", "https://github.com/GoogleCloudPlatform/microservices-demo",
     "c7cb6d5bfd6ea3aed768634ebbcb98cb7a523712"),
    ("django-payments", "https://github.com/jazzband/django-payments", "5607e9e88762df9831980832c194f49b227dbe93"),
]
DP_AFTER = "47449a1516772e3996060d77efa1ab970ad0dcd1"   # last django-payments commit tested after the 18 Oct map
PR501 = "529d6a5"


# Child Pythons write UTF-8 even when their output is a pipe (Windows would otherwise use cp1252
# and crash on characters such as "·", "→" or "✓").
CHILD_ENV = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}


def run(cmd, log=None, cwd=None, env=None):
    start = time.monotonic()
    proc = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, cwd=cwd, env=env or CHILD_ENV,
                          encoding="utf-8", errors="replace")
    wall = time.monotonic() - start
    text = JOB_ID.sub("<JOB_ID_REDACTED>", proc.stdout + proc.stderr)
    if log:
        log.write_text(f"$ {' '.join(map(str, cmd))}\n{text}\n[exit {proc.returncode}, wall {wall:.1f} s]\n",
                       encoding="utf-8")
    return proc.returncode, text, wall


def venv_python(venv):
    return venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    for tool in ("git",):
        if not shutil.which(tool):
            sys.exit(f"{tool} is not on PATH. Install it and open a new terminal.")
    if sys.version_info < (3, 11):
        sys.exit(f"Python 3.11+ is required (this is {platform.python_version()}).")
    OUT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    print(f"Work folder: {WORK}\nEvidence:    {OUT}")
    venv = WORK / "venv"
    if not venv.exists():
        run([sys.executable, "-m", "venv", venv])
    py = venv_python(venv)
    run([py, "-m", "pip", "install", "--upgrade", "pip"])
    _, _, t_install = run([py, "-m", "pip", "install", "--upgrade", "unvibecode"], OUT / "pip_install.log")
    run([py, "-m", "pip", "install", "--upgrade", str(ROOT / "prototype")], OUT / "pip_install_prototype.log")
    _, version, _ = run([py, "-m", "unvibecode", "--version"])
    _, health, _ = run([py, "-m", "unvibecode", "health"], OUT / "health.log")
    _, pyver, _ = run([py, "--version"])
    env_lines = [f"- OS: {platform.platform()}", f"- Python: {pyver.strip()}",
                 f"- unvibecode: {version.strip()} (install {t_install:.1f} s)", f"- health: {health.strip()}"]

    rows, business_pages = [], {}
    for name, url, commit in TARGETS:
        repo = WORK / "repos" / name
        if not repo.exists():
            run(["git", "clone", "-q", "--filter=blob:none", url, repo])
        run(["git", "-C", repo, "checkout", "-q", commit])
        results = WORK / "results" / f"{name}_{STAMP}_{int(time.time())}"
        code, text, wall = run([py, "-m", "unvibecode", "review", "--repository", repo, "--output", results,
                                "--no-open-browser"], OUT / f"run_{name}.log")
        status = next(iter(results.rglob("analysis-status.json")), None)
        fast = full = reason = "?"
        if status:
            s = json.loads(status.read_text(encoding="utf-8"))
            fast = f"{s['lanes']['FAST_LANE']['status']} ({s['lanes']['FAST_LANE'].get('duration_seconds')} s)"
            full = s["lanes"]["FULL_ANALYSIS"]["status"]
            reason = (s["lanes"]["FULL_ANALYSIS"].get("customer_reason") or "").split(".")[0]
        page = next(iter(results.rglob("business-workflows.html")), None)
        if page:
            business_pages[name] = page
        summary = re.search(r"UNVIBECODE REVIEW [A-Z]+ · \d+s", text)
        rows.append(f"| {name} | `{commit[:8]}` | {wall:.1f} s | {summary.group(0) if summary else '?'} | {fast} | "
                    f"{full} | {reason or '-'} | {'yes' if page else 'no'} |")
        print(rows[-1])

    # Prototype: tests, then the django-payments demo.
    proto = ROOT / "prototype"
    tcode, ttext, _ = run([py, "-m", "unittest", "discover", "-s", "tests"], OUT / "prototype_tests.log", cwd=proto)
    dp = WORK / "repos" / "django-payments"
    dp_map = OUT / "django-payments_UNVIBECODE.md"
    workflows = business_pages.get("django-payments") or proto / "fixtures" / "django-payments_5607e9e_business-workflows.html"
    run(["git", "-C", dp, "checkout", "-q", TARGETS[-1][2]])
    run([py, "-m", "unvibecode_mapfile", "build", "--repository", dp, "--workflows", workflows, "--map", dp_map],
        OUT / "django-payments_build.log")
    run(["git", "-C", dp, "fetch", "-q", "origin"])
    lines = []
    for c in run(["git", "-C", dp, "rev-list", "--reverse", f"{TARGETS[-1][2]}..{DP_AFTER}"])[1].split():
        subject = run(["git", "-C", dp, "log", "-1", "--format=%s", c])[1].strip()
        line = run([py, "-m", "unvibecode_mapfile", "impact", "--repository", dp, "--map", dp_map,
                    "--base", f"{c}~1", "--head", c, "--oneline"])[1].strip()
        lines.append(f"{c[:7]} {subject}\n    {line}")
    (OUT / "django-payments_after_18_oct.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    # PR #501 as an uncommitted change. Its two payments/ files were not touched by any other commit
    # between 5607e9e and 529d6a5, so taking their #501 versions equals applying its diff (and avoids
    # `git apply` failing on Windows CRLF checkouts).
    pr_files = run(["git", "-C", dp, "diff", "--name-only", f"{PR501}~1", PR501, "--", "payments/"])[1].split()
    run(["git", "-C", dp, "checkout", "-q", PR501, "--", *pr_files])
    _, demo, demo_wall = run([py, "-m", "unvibecode_mapfile", "impact", "--repository", dp, "--map", dp_map],
                             OUT / "django-payments_unvibe_PR501_uncommitted.log")
    run(["git", "-C", dp, "checkout", "-q", "HEAD", "--", "."])

    ran_match = re.search(r"Ran \d+ tests", ttext)
    ran = ran_match.group(0) if ran_match else "?"
    (OUT / "SUMMARY.md").write_text("\n".join([
        f"# Re-run of the UnvibeCode trial ({datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC)",
        "", "## Environment", *env_lines, "",
        "## UnvibeCode runs (`python -m unvibecode review --repository <repo> --output <dir> --no-open-browser`)", "",
        "| Repository | Commit | Wall | CLI summary | Code-map lane | Business lane | Reason | Business Workflow Map produced |",
        "|---|---|---|---|---|---|---|---|", *rows, "",
        "## Prototype", f"- Tests: {'passed' if tcode == 0 else 'FAILED'} ({ran})",
        f"- django-payments workflows used: {'this run (UnvibeCode business analysis worked)' if 'django-payments' in business_pages else 'UnvibeCode published sample (business analysis unavailable in this run)'}",
        f"- `unvibe` on PR #501 as an uncommitted change: {demo_wall * 1000:.0f} ms", "", "```", demo.strip(), "```", "",
        "Commits after the 18 Oct map: see django-payments_after_18_oct.txt",
    ]) + "\n", encoding="utf-8")
    print(f"\nDone. Read {OUT / 'SUMMARY.md'}")
    if business_pages:
        print("UnvibeCode business analysis WORKED for: " + ", ".join(business_pages) +
              ". Update the answer's '10 of 10 runs failed' sentence with your own result.")


if __name__ == "__main__":
    main()
