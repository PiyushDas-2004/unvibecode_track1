"""Point every link in this repository at your own GitHub repository.

Usage:  python scripts/set_repo_url.py YOUR_USER/YOUR_REPO [BRANCH]      (BRANCH defaults to main)
"""
import sys
from pathlib import Path

OLD_TREE = "https://github.com/PiyushDas-2004/unvibecode/tree/claude/unvibecode-track2-adoption-yqgmiv"
OLD_PIP = "git+https://github.com/PiyushDas-2004/unvibecode@claude/unvibecode-track2-adoption-yqgmiv"
OLD_CLONE = "https://github.com/PiyushDas-2004/unvibecode.git"

repo, branch = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "main")
new = {OLD_TREE: f"https://github.com/{repo}", OLD_PIP: f"git+https://github.com/{repo}@{branch}",
       OLD_CLONE: f"https://github.com/{repo}.git"}
root = Path(__file__).resolve().parent.parent
for path in root.rglob("*"):
    if path.is_file() and ".git" not in path.parts and path.suffix in {".md", ".yml", ".py", ".txt"} \
            and path.name != "set_repo_url.py":
        text = path.read_text(encoding="utf-8", errors="ignore")
        updated = text
        for old, rep in new.items():
            updated = updated.replace(old, rep)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            print("updated", path.relative_to(root))
