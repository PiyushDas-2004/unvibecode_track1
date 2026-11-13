# User journey: heard of it → ran it once → runs it every week

Each stage lists what the developer does, what happened in my trial, and where people drop off. "F##" refers to [friction_log.md](friction_log.md). "Hypothesis" marks reasoning that I did not observe directly.

## Stage 0: Hears about it
- **Trigger:** a challenge post, the GitHub README, a teammate.
- **What they read:** "Reverse engineer a complex codebase into business workflows…", four outputs, sample reports.
- **Drop-off risk:** low. The pitch is clear and the sample reports are public.

## Stage 1: Installs (time-to-install 5 s)
- `python -m pip install --upgrade unvibecode` → 10 kB wheel, no dependencies (F01).
- **Drop-off risk:** low on x86 Python 3.11+. Issues #411 and #543 report older platform-wheel problems. Those are fixed in 0.4.0 by going pure-Python.

## Stage 2: First run (time-to-first-output 11–26 s)
- Types the long command with an absolute path. Code is uploaded; the terminal dashboard updates; the browser opens.
- **Observed:** Code Map + Context arrive in seconds. Business Workflow Map and Risk Findings fail with "exhausted its API credits" (F04). Java gets nothing (F09). TS gets an almost empty map (F10).
- **Drop-off point A, "the headline output is missing".** The README sells business workflows and risks; on the day I tried, the run delivered neither. #291's author: "After that, I had no clear reason to open the tool again."

## Stage 3: Explores the report (minutes)
- Browser page with an all-files graph and a file picker (F07). The first file listed is a wrongly connected test fixture (F08).
- **Value moment:** clicking a file and downloading "Optimal connection context" for an AI assistant. #291's author called the Connected Code Map "the best part … I couldn't see easily in VS Code".
- **Drop-off point B, "I looked at it, now what?"** The report answers questions the user had *today* about *this* repo. It is a document to read once. No action is left to take, so there's no reason to come back to it.

## Stage 4: Day 2, the would-be second run
- **Trigger needed:** something has to remind them, and nothing does. No file in the repo, no hook, no command in muscle memory.
- **Observed if they do re-run:** same 15–25 s upload, new timestamped folder, no "what changed", no memory of yesterday (F11–F14). Output is byte-identical, but the user can't tell (F13).
- **Drop-off point C, "re-running tells me nothing new".** With no memory of the previous run, a re-run can't answer "what changed", which is the main question someone has on day 2.

## Stage 5: Weekly use (where the product needs people to be)
For a developer to come back weekly, the product has to:
1. **Be triggered by something that already happens weekly.** Code review, merging, pulling teammates' work and onboarding someone all happen weekly; "I feel like analysing a repo" doesn't.
2. **Answer a question about change.** Most of a developer's week is spent changing code that already exists, not reading new repos.
3. **Remember yesterday.** The second run should be more useful than the first.
4. **Leave the name somewhere the team sees it.** Today the name lives in a local browser tab that gets closed.
5. **Not need an upload or the LLM each time.** The LLM stage was down in my trial, and the hosted service has 2 slots.

## Persona drop-off summary

| Persona | Likely trigger | Drops at | Why |
|---|---|---|---|
| OSS first-time contributor | "I want to fix an issue in repo X" | B | One-off: after the first PR they know the area. |
| New hire on a team repo | Day 1 onboarding | A or B, or never starts | May not be allowed to upload private code (F17); the report is read once. |
| Team developer, Python/Go | Daily changes, PR reviews | C | Nothing ties the tool to change or review. |
| Team developer, TS/Java | Same | A | The map is near-empty or empty (F09, F10). |
| Tech lead | Architecture drift, reviews | C | No history and no way to see when a dependency appeared. |
| AI-assisted ("vibe") coder | After an assistant writes a large change | B/C | Has to re-run and re-read the whole graph to see what the assistant touched (hypothesis, consistent with the README's AI-generated-code pitch). |

## Main insight

UnvibeCode is built for the moment a repo is **unfamiliar**, and that moment happens once per repo per person. To get repeat use, the product has to cover the way a repo becomes unfamiliar again every week as **its structure changes**: teammates merge, an assistant writes code, a refactor lands. The tool already computes structure deterministically. It doesn't keep that structure anywhere the team will see it change.
