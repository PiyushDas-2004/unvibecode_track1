"""Estimate how often commits change internal import structure (proxy for 'the code map changed').
Usage: python import_churn.py REPO_DIR PKG_PREFIX[,PREFIX2] [N_COMMITS]
Counts non-merge commits whose diff adds/removes a Python import line that refers to an internal module
(relative import, or absolute import starting with one of the given package prefixes)."""
import re, subprocess, sys, datetime
repo, prefixes = sys.argv[1], sys.argv[2].split(',')
n = int(sys.argv[3]) if len(sys.argv) > 3 else 200
log = subprocess.run(['git','-C',repo,'log',f'-{n}','--no-merges','--format=@@C %H %ct','-p','--unified=0','--','*.py'],capture_output=True,text=True).stdout
pat = re.compile(r'^[+-]\s*(from\s+(\.\S*|(%s)\S*)\s+import|import\s+(%s)\S*)' % ('|'.join(map(re.escape,prefixes)),'|'.join(map(re.escape,prefixes))))
commits = []; cur=None
for line in log.splitlines():
    if line.startswith('@@C '):
        _,h,t = line.split(); cur={'h':h,'t':int(t),'imp':False}; commits.append(cur)
    elif cur and (line.startswith('+') or line.startswith('-')) and not line.startswith(('+++','---')):
        if pat.match(line): cur['imp']=True
total = subprocess.run(['git','-C',repo,'log',f'-{n}','--no-merges','--format=%ct'],capture_output=True,text=True).stdout.split()
span_days = (int(total[0])-int(total[-1]))/86400 if total else 0
window = set(subprocess.run(['git','-C',repo,'log',f'-{n}','--no-merges','--format=%H'],capture_output=True,text=True).stdout.split())
commits = [c for c in commits if c['h'] in window]
py = len(commits); imp = sum(c['imp'] for c in commits)
weeks = max(span_days/7,1e-9)
print(f"{repo}: last {len(total)} non-merge commits over {span_days:.0f} days; {py} touch .py; {imp} change internal imports "
      f"({imp/len(total):.0%} of commits; {imp/weeks:.1f} per week)")
