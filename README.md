# `unvibe`: business-workflow reach for every change
### UnvibeCode Engineering Challenge 2026, Cohort 3, Track 2 (Developer Adoption & Repeat Usage)

**Proposal:** `unvibe` is the command a developer types right after they, or their AI assistant, change code. It answers in UnvibeCode's own vocabulary which **business workflows** the change touched, in about 0.1 s, offline. It reads a committed `UNVIBECODE.md` that stores the Business Workflow Map and the Connected Code Map. Every pull request shows the same one-line answer as a quiet **UnvibeCode** check.

- Answer as submitted to the form: [`submission/form_answer_full.md`](submission/form_answer_full.md) ([compact](submission/form_answer_compact.md), [micro](submission/form_answer_micro.md))
- Working prototype (stdlib Python, 38 passing tests on real UnvibeCode output): [`prototype/`](prototype/)
- Trial evidence: [`evidence/README.md`](evidence/README.md) · business-reach verification: [`evidence/business_reach_verification.md`](evidence/business_reach_verification.md)

> This is a **community entry, not an official UnvibeCode product**. No UnvibeCode code is copied here.

## Example: django-payments PR #501, as an uncommitted change

```
$ unvibe
UnvibeCode business reach: this change touches 1 business workflow(s)
  provider-backed payment checkout and callback handling [Payment workflows]: changed StripeProviderV3, StripeProviderV3.create_session, StripeProviderV3.get_form in payments/stripe/providers.py
Code reach: 2 changed file(s); 1 other file(s) import them directly.
...
[76 ms, nothing uploaded]
```

On the PR, in the checks list: `UnvibeCode · 1 business workflow(s): provider-backed payment checkout and callback h… · 1 direct importer(s)`

## Why this answer: the brief, read line by line

| The brief says | My trial showed | So the design does |
|---|---|---|
| MCP is not enough: users "benefit … without remembering its name or deliberately returning to it" | Nothing in 0.4.0 brings a user back. Each run re-uploads, makes a new folder and opens an all-files graph. | The developer **types the name** at a moment they already have: after an AI or human edit, before committing. |
| "memorable as a product" | UnvibeCode's distinctive output is the **Business Workflow Map**. Its import graph is something other tools can also produce. | Answers come in **workflow names**, e.g. "PayPal checkout and post-payment reconciliation". |
| "useful during daily development … return tomorrow" | AI-written code makes code unfamiliar every day, which is UnvibeCode's own pitch ("Your LLM helped write 100,000 lines…"). | Every change, from either person or AI, is a trigger, and every PR repeats the line. |
| "easy to access" | The hosted LLM stage failed **10/10** runs ("exhausted its API credits"). The code-map lane succeeded every time in 1.5–3.7 s, byte-identical on re-runs. | The LLM only **refreshes** the committed index (weekly), and a failed refresh **keeps** the old one. Each answer is a local lookup: no upload, no wait, works on private code once the file exists. |

Verified on real history: I built the map at django-payments' 18 Oct commit, then checked all 8 commits merged afterwards by hand. All 8 were classified correctly (5 touched a workflow), after fixing two matcher bugs that the check found.

## How I got here

The first answer (passes 1–3) was an import-graph "lockfile" checked in CI. Re-reading the brief (pass 4) showed it repeated the MCP flaw (value without deliberate return) and wasn't specific to UnvibeCode. See [`ideation/pass_04.md`](ideation/pass_04.md) for the gap analysis and alternatives, and [`scoring/rubric_matrix.md`](scoring/rubric_matrix.md) for scores: the final answer 88, the earlier answer re-scored to 80.

## Repository layout

| Path | Contents |
|---|---|
| `evidence/` | Logs of every run (job IDs redacted), timings, accuracy checks against source, determinism and cross-commit tests, import-churn and upload-gate data, business-reach verification, upstream issue/PR index, screenshots |
| `research/` | `upstream_audit.md`, `user_journey.md`, `friction_log.md` (22 timestamped entries), `competitor_landscape.md` (cited) |
| `ideation/` | `candidate_ledger.csv` (218 entries), `pass_01`–`pass_05.md`, `crowded_ideas.md`, `redteam.md` (3 rounds), `progress_log.md` |
| `scoring/` | `rubric_matrix.md` on the official 35/25/20/10/10 rubric |
| `prototype/` | `unvibecode-mapfile` + `unvibe` / `git unvibe`, tests, real examples, CI and Claude Code slash-command examples, measurement plan, limitations |
| `scripts/` | `reproduce_trial.py` re-runs the whole trial and the prototype demo on any machine and writes `evidence/rerun_<date>/`; `set_repo_url.py` rewrites the repository links |
| `submission/` | Form answers (full 439 words, compact 222, micro 123) and `self_score.md` |

## Reproduce the trial on your machine

```bash
python scripts/reproduce_trial.py      # Python 3.11+, git, internet; about 2–3 minutes
```

This runs UnvibeCode on the 5 pinned public repositories, then the prototype tests and the django-payments `unvibe` demo, and writes `evidence/rerun_<date>/SUMMARY.md`. Job IDs are redacted.

## Run the prototype (no network)

```bash
git clone https://github.com/PiyushDas-2004/unvibecode.git
cd unvibecode/prototype
python -m unittest discover -s tests
python -m unvibecode_mapfile build --bundle fixtures/django-payments_5607e9e.zip \
    --workflows fixtures/django-payments_5607e9e_business-workflows.html --map /tmp/UNVIBECODE.md
```

See [`prototype/README.md`](prototype/README.md) to reproduce the PR #501 example and run it live on your own repo.

License: MIT.
