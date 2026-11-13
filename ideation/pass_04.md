# Pass 4: re-reading the brief, finding the gaps in v1, and upgrading the answer

Trigger for this pass: the question "did you thoroughly go through the Track 2 problem?" I re-fetched the brief on 13 Nov 2026 15:4x UTC (unchanged) and graded v1 (K1b, the committed import-graph map) against **each phrase of the brief**, not only the rubric.

## 1. The brief, phrase by phrase, against v1

| Phrase in the brief | What it asks for | v1 (K1b) | Gap |
|---|---|---|---|
| "not yet readily accessible through enough of the **channels and formats** developers use in their everyday workflows" | A channel and a format | Repo file + CI | OK |
| MCP is not enough because users benefit "**without remembering its name or deliberately returning to it**" | The user must **deliberately** invoke it and **remember the name** | Value arrives through a CI job. GitHub job summaries sit behind the Actions tab. Nobody types or chooses "UnvibeCode". | **G1, serious.** v1 repeats the flaw the brief pins on MCP: it is automation that works without the developer coming back. |
| "**memorable as a product**" | What people remember must be *UnvibeCode's* value | The file holds an import graph. import-linter, madge or dependency-cruiser could produce the same thing. UnvibeCode's identity ("Business Workflow Map", "Trace what the business actually does") is absent. | **G2, serious.** Brand recall attaches to a filename, not to anything only UnvibeCode does. |
| "**easy to access**" | Low effort for an individual | Needs repo write access + CI setup + a team decision to commit a generated file | **G3.** Most of the "1,000+ developers" are likely individuals; they can't adopt a team artifact alone. |
| "useful during **daily** development" … "return **tomorrow** or next week" | A daily touchpoint | Per PR (team), per structural PR (rarer) | **G4.** Not daily for a solo developer. |
| "Think beyond acquiring more first-time users" | Retention, not acquisition | Yes | OK |
| "Consider the developer's **trigger** … how quickly they can access **value**" | Trigger + time-to-value | PR trigger, 0.1 s local | OK |

**Re-score of v1 under this stricter reading:** R 27 (automated, hidden summary), W 21, F 17, B 7 (generic graph, hidden surface), O 8 = **80** (was 84).

## 2. What else the evidence says that v1 ignored

- **The daily moment UnvibeCode was built for is now AI-written code.** Its README headline: "Your LLM helped write 100,000 lines of code. Now how do you understand what it actually built?" The product name is a verb against vibe coding. Every AI-assistant session produces code its developer didn't write, so the "unfamiliar code" moment now recurs **daily**, not once per repo. (Supporting, verified: Murphy-Hill et al., arXiv 2607.01418, on tens of thousands of Microsoft engineers adopting Claude Code / Copilot CLI in early 2026. Retention tracked coding activity.)
- **UnvibeCode already publishes a real Business Workflow Map with machine-usable references.** The django-payments sample (docs/gitdocs/django-payments/2026-10-18) lists 7 workflows. Each has `Symbol · file · lines` references. I checked 6 of them against django-payments `5607e9e` (the last commit on or before 18 Oct 2026) and all 6 match line for line (e.g. `payments/core.py:146 def capture`).
- **The LLM stage is expensive and was down for my whole trial** (10/10 runs to 15:48 UTC), and it is non-deterministic (#408). So business analysis must not run per PR or per commit. But a **stored** workflow index can be looked up deterministically and for free.

## 3. Alternatives generated against the gaps

| ID | Idea | Gaps fixed | R | W | F | B | O | Total | Crowd |
|---|---|---|---|---|---|---|---|---|---|
| v1 | K1b, import-graph lockfile + CI summary | – | 27 | 21 | 17 | 7 | 8 | 80 | 3 |
| A | v1 + **Business Workflow index in the file**; every PR's **check title** names the business workflows it touches | G2, part of G1 | 29 | 21 | 16 | 10 | 9 | 85 | 3 |
| B | **`unvibe`**: a typed command (terminal and agent slash command) that answers "what did this change touch, in business terms?" for uncommitted / AI-written code, from the stored map, offline | G1, G3, G4 | 27 | 20 | 16 | 9 | 7 | 79 | 5 (#312 proposed an `unvibe` alias for a pre-commit hook) |
| **A+B** | **One stored UnvibeCode map with business workflows; two entry points: the developer deliberately types `unvibe` (daily, after an AI session or before committing), and the PR check repeats the same "business reach" line for the reviewer** | G1–G4 | **31** | **22** | 16 | **10** | **9** | **88** | 3 |
| C | DeepWiki/gitingest-style URL swap (`github.com/x/y` → UnvibeCode page) | G3, brand | 20 | 23 | 13 | 10 | 4 | 70 | 6 |
| D | `/unvibe` slash command inside assistants only, no stored artifact | G1 | 24 | 20 | 14 | 7 | 5 | 70 | 7 |
| E | VS Code CodeLens "part of Workflow: Refund" above functions | G2, G4 | 27 | 22 | 11 | 9 | 6 | 75 | 8 |

C is an acquisition play (first-time users), and the brief says to look past those. Each visit to a new repo is a fresh first use. D has the same problem as MCP once the user stops typing it: nothing persists, so nothing accumulates. E is the strongest single surface, but it is the most-proposed channel and needs an extension, a hosted wait and per-editor work. It can read the same stored file later.

## 4. Red team on A+B

**Founder.** *"You now depend on the LLM stage that was down all week."*
Only the weekly or per-release refresh of the workflow index uses the LLM. Per-PR and per-`unvibe` answers are lookups in the committed file (no LLM, no upload). If a refresh fails, the previous workflow section is **kept**, not erased. I verified this in the prototype. So an outage degrades freshness instead of breaking the daily loop. Cost falls from "one LLM run per PR" to "one per repo per week".

**Founder.** *"Is 'workflow touched' accurate?"*
I tested it on real django-payments PRs merged **after** the sample date (see prototype/examples/django-payments). I checked every hit by hand.

**Rival (#683 PR business impact, #312 `check --staged`).**
#683 re-runs the LLM per PR. #312 uploads at commit time. A+B does neither. It also gives the user a reason to *type the name*, which neither of them does.

**Jaded engineer.** *"Another PR bot."*
No comment is posted. The output is a one-line check-run title in the checks list, which is warn-only. The deliberate `unvibe` command is opt-in.

**Jaded engineer.** *"Workflow names from an LLM will churn and spam diffs."*
The index refreshes only on purpose (weekly or per release). It never refreshes on every PR, so its diff appears in one reviewable PR a week.

**Verdict:** A+B survives. Its main residual risk is that daily `unvibe` use is a hypothesis about developer behaviour, which the experiment is designed to test (manual runs are counted separately).

## 5. Convergence

Pass 4 found a candidate that beats the previous leader by 8 points (88 vs 80 on the stricter reading). A **pass 5** re-ran the search on the new leader (see pass_05.md). It found no candidate within 5 points, so the loop is converged again with A+B as the leader.
