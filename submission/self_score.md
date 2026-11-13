# Self-score (harsh judge) and QA

## Round 3 (current answer, after pass 4 re-read the brief)

The first two rounds below graded the earlier answer (an import-graph lockfile checked in CI). When I re-read the brief phrase by phrase, it failed two of the brief's own tests. Its value arrived through automation, so users could "benefit … without remembering its name or deliberately returning", which is the exact flaw the brief pins on MCP. And its output was a generic import graph, not something "memorable as a product". The current answer fixes both.

| Criterion | Max | Score | Harsh-judge justification |
|---|---|---|---|
| Repeat usage | 35 | 31 | A deliberate daily trigger (after an AI or human change) plus a per-PR echo. The metric counts manual runs separately, so automation can't fake the habit. −4 because daily manual use is a hypothesis I couldn't test on real users. |
| Workflow fit / access | 25 | 22 | Terminal, git and the PR checks list. One `build`, then offline. Readable with nothing installed. −3 for the hosted refresh and the upload approval it needs. |
| Feasibility | 20 | 16 | Working prototype with 38 tests, verified on real later commits. −4 because the workflow refresh depends on an LLM stage that was down throughout my trial (mitigated by keeping the last index), and only Python matching is exact. |
| Brand recall | 10 | 10 | The name is typed, shown in the PR checks list, and carried by UnvibeCode's own nouns (business workflows). |
| Original reasoning | 10 | 9 | Trial-driven mechanism. Surface overlap with #683 and #312. |
| **Total** | 100 | **88** | |

### Weakest points and what I did about them
1. **No Business Workflow Map from my own runs.** The LLM stage failed 10/10. I used UnvibeCode's own published django-payments map and verified 6/6 of its references against the matching commit. The README and fixtures say so plainly.
2. **Matcher errors.** The hand-check on real commits found two (d1eea51, ff5082a). Both are fixed and covered by regression tests; 8/8 correct afterwards.
3. **"Formatting-only edits count as touched."** Disclosed as a limitation.
4. **Daily manual use is unproven.** It is the experiment's primary metric, with a kill threshold.

## Claim → evidence trace (current form_answer_full.md)

| Claim | Evidence |
|---|---|
| "in about 0.1 s, offline" / "In 76 ms" | prototype/examples/django-payments/unvibe_uncommitted_log.txt (76 ms; 68–100 ms in the other logs) |
| PR #501 output text | same log |
| "failed on 10 of 10 runs ('exhausted its API credits')" | evidence/run1_flask.log, run1_node-express…, run1_microservices…, run2_flask…, run_flask_{pre_query,d73fa1c,c2705ff_parent,c2705ff}.log, run_flask_retry_llm.log, run_flask_retry2_llm.log |
| "Connected Code Map succeeded every time in 1.5–3.7 s, with byte-identical re-runs" | evidence/raw_outputs/*/analysis-status.json FAST_LANE; evidence/README.md §4 |
| "a failed refresh keeps the previous index" | test `KeepsWorkflowsWhenBusinessAnalysisIsDown` |
| "all 8 commits merged afterwards … classified correctly (5 touched a workflow) … after fixing two matching bugs" | evidence/business_reach_verification.md; examples/django-payments/after_18_oct_log.txt; tests `ChangeToWorkflow` |
| "PayPal checkout and post-payment reconciliation" | examples/django-payments/UNVIBECODE.md (from UnvibeCode's sample) |
| "43 Flask files whose `import flask` resolves to a test fixture" | evidence/README.md §5; examples/flask/UNVIBECODE.md |
| "38 passing tests" | `python -m unittest discover -s tests` from a fresh clone |

---

# Earlier rounds (previous answer, kept for the audit trail)


## Round 1: grading the first draft of form_answer_full.md

| Criterion | Max | Score | Harsh-judge justification |
|---|---|---|---|
| Likelihood of real repeat usage | 35 | 27 | Every PR is a trigger, which is strong. But the draft's success metric ("3+ runs a week") would count CI runs, so a bot could produce the "habit". The draft also didn't say what happens on repos whose imports rarely change. |
| Workflow fit and ease of access | 25 | 20 | Lives in PRs and the repo tree; reading needs no install. A judge will ask whether teams accept a generated file in git, and the draft doesn't answer. |
| Feasibility and specificity | 20 | 18 | Named commands, a working prototype, 23 tests, real outputs. Depends on the hosted service for refresh, and that is not stated in the answer. |
| Brand recall | 10 | 9 | Filename next to README.md, PR diffs, check name. Recall is argued by the lockfile analogy, not measured. |
| Original reasoning | 10 | 8 | The mechanism rests on trial evidence nobody else has (line-free keys stable, LLM down, gate data). "PR impact" overlaps public issue #683 on surface. |
| **Total** | 100 | **82** | |

### Weakest points found
1. The repeat-usage metric could be met by automation alone.
2. The draft was 480 words, over the 350–450 target.
3. Nothing on teams that refuse generated files.
4. The language limits (TS/Java) were not reflected in the test cohort.
5. One wordy sentence per point; the submission rules ask for short sentences.

### Fixes applied
1. Metric changed to "3+ runs a week, **at least one started by hand**" in the form and in prototype/README.md (manual and CI runs counted separately).
2. Trimmed to 446 words plus the link line.
3. Warn-only default, a `linguist-generated` diff-collapse line and a no-commit fallback are in the prototype README and red team. The form says "warn-only" (no room for more).
4. Test cohort restricted to "active Python/Go repos", the languages where my trial showed the map is mostly right.
5. Sentences shortened. MCP contrast compressed to one clause.

## Round 2: grading the final answer

| Criterion | Max | Score | Justification |
|---|---|---|---|
| Repeat usage | 35 | 29 | Triggers on every PR without anyone having to remember. Structural refresh rhythm measured on real repos (6%/37%). Value accumulates through git history. The metric separates manual from automated runs. Still unproven with real users: the per-PR reach line's usefulness on small PRs is a hypothesis. |
| Workflow fit | 25 | 21 | PR job summary, repo tree and git log are existing surfaces. No new app. Warn-only. Reading the file needs no upload permission. CI setup and a one-time upload approval remain. |
| Feasibility | 20 | 18 | Thin layer over the existing context ZIP. Prototype builds and passes tests from a fresh clone. The CI template was not run on GitHub Actions. |
| Brand | 10 | 9 | As above. |
| Originality | 10 | 8 | As above. |
| **Total** | 100 | **85** | |

## QA checklist

| Check | Result |
|---|---|
| One approach, not a list | Yes. One artifact (`UNVIBECODE.md`) with one CLI and one PR check; `impact` and `check` are two readings of the same file. No other channels proposed. |
| Every claim traces to evidence | See the table below. |
| README renders | Checked on github.com after push (see final report). |
| Prototype runs from a fresh clone | Yes. Cloned the pushed branch into an empty folder: `python -m unittest discover -s tests` → 23 tests OK; quickstart steps 2–3 reproduced the +3/−2 delta; total 2 s. `pip install ./` and the `git+https://…#subdirectory=prototype` install from the CI example both produced a working `unvibecode-mapfile 0.1.0`. |
| No secrets or personal data | `git grep` for tokens, keys, private-key headers, emails and 32-hex job IDs: no hits. The upstream public preview token is not reproduced. Job IDs in logs are replaced by `<JOB_ID_REDACTED>`. |
| Word counts | full 452 total (446 + link line), compact 242, micro 130. |

## Claim → evidence trace (form_answer_full.md)

| Claim | Evidence |
|---|---|
| "`helpers.py` has 12 direct importers; changed `flash` is used by the tutorial's `auth.py` and `blog.py`" | prototype/examples/flask-refactor-c2705ff/run_log.txt, Step 3 |
| "computed … in under 0.1 s, with no upload" | same log: 91 ms; flask-gate/run_log.txt: 95 ms, 68 ms |
| "6% of Flask and 37% of NetBox commits" | evidence/import_churn.txt |
| "business stage failed on 9 of 9 runs ('exhausted its API credits')" | evidence/run1_flask.log, run1_node-express…, run1_microservices…, run2_flask…, run_flask_{pre_query,d73fa1c,c2705ff_parent,c2705ff}.log, run_flask_retry_llm.log (9 runs that reached business analysis; spring-petclinic was skipped earlier for language support) |
| "Connected Code Map lane succeeded every time in 1.5–3.7 s" | `FAST_LANE.duration_seconds` in evidence/raw_outputs/*/analysis-status.json (1.516–3.666 s); FAST_LANE COMPLETED in every run log |
| "byte-identical results on re-runs" | evidence/README.md §4 (cmp of all bundle files, md5 of graph data) |
| "Flask's map did not change across two multi-commit ranges" | evidence/README.md §4; test `StabilityAcrossCommits` |
| "c2705ff, 36 files … exactly +3/−2 … 30-line diff" | examples/flask-refactor-c2705ff/run_log.txt (36 changed files, +3/−2), git_style_diff.txt (30 lines) |
| "gate skipped 14 of Flask's last 25 commits to `src/`" | evidence/gate_decisions_flask.txt |
| "43 Flask files' `import flask` statements resolve to a 3-line test fixture" | evidence/README.md §5; examples/flask/UNVIBECODE.md "Check these connections" |
| "about 550 lines of stdlib Python with 23 passing tests" | `wc -l prototype/unvibecode_mapfile/*.py` (≈550); unittest output |
| "an MCP call would hide the name" | the challenge brief (evidence/challenge_doc_cohort3.md) |
