# Upstream audit: FinanceFlash/unvibecode

Sources: the upstream repo cloned at `c75b75e2` (4 Nov 2026); the installed wheel `unvibecode==0.4.0` (source read, not copied); the PyPI JSON API ([evidence/pypi_release_history.txt](../evidence/pypi_release_history.txt)); and all 650 issues and 110 PRs from the GitHub search API on 13 Nov 2026 ([evidence/upstream_issues_index.tsv](../evidence/upstream_issues_index.tsv), [evidence/upstream_pull-requests_index.tsv](../evidence/upstream_pull-requests_index.tsv)).

## 1. Access channels that exist today

| Channel | State | Notes |
|---|---|---|
| CLI `unvibecode` / `python -m unvibecode` | Shipped | `health`, `review --repository PATH [--dry-run] [--output DIR]`, `resume JOB_ID`, plus the hidden `--no-open-browser`. `--repository` is required, so there is no current-directory default. |
| Python library | Not a public API | The package is an HTTP client (`client.py`), a zip packer (`archive.py`) and terminal rendering. Nothing is documented for import. |
| Hosted HTTP API | Undocumented but used by the CLI | `POST /jobs` (zip), `GET /jobs/{id}?after=`, `/download`, `/interim`, `/health` at `shipready-api.alphashots.ai/analysis`. Public preview token is hard-coded. Job ID = bearer reference. |
| HTML report | Shipped | `<repo>-unvibecode-full.html` (tabs: Connected Code, LLM Context; plus Business Workflows / Risk Findings when the LLM stage succeeds). Opens in the browser automatically. |
| Repository context ZIP | Shipped | `manifest.json`, `chunks.jsonl`, `connections.jsonl`, `selections.jsonl`, `unresolved_relationships.jsonl`, `README.md`. **The only machine-readable output.** |
| Published sample reports | Shipped | GitHub Pages under `docs/gitdocs/` (smolagents, PocketFlow, mini-swe-agent, django-payments; dated 2026-10-18). |
| Agent "skills" | Shipped as docs | `skills/` holds 9 instruction packs (RAG review, guardrails, LLM routing…). They say they are "not the UnvibeCode parser, MCP server". |
| Workflow packs | Shipped as docs | `prebuilt-workflow-paths/`: 18 business workflow checklists. Issue #457 notes the CLI does not use them. |
| MCP server | Not shipped | Mentioned in issues #56, #111, #506, #629, and in the challenge brief as the obvious-but-insufficient answer. |
| CI / GitHub Action / IDE / pre-commit | Not shipped | Proposed in issues #312, #476, #472, #683, #457. |

## 2. Output formats and configuration

- Config options: only `--output` and `UNVIBECODE_API_URL` (env). No config file, no ignore file, no format flag.
- Output: a new timestamped folder per run. Exit code 1 when any lane is partial (evidence: all 9 runs).
- File limits (wheel README): 50 MiB compressed, 200 MiB extracted, 10,000 files, 10 MiB per file, 1-hour timeout. LIMITATIONS.md: business review is skipped above about 2 million estimated tokens.
- Determinism: the code-map lane is byte-identical across runs (my trial). The LLM lane is reported as non-deterministic (#251, #408, #516).

## 3. Release history and an important direction change

17 releases from 0.3.0 (30 Jul 2026) to 0.4.0 (8 Nov 2026). Versions 0.3.9–0.3.15 shipped platform-specific wheels, which fits with local native parsing. Issue #289's author reports that on 0.3.15 "the local Connected Code and repository-context stages completed". **0.4.0 is a pure-Python 10 kB client that uploads all selected source files**, and the wheel README says so. Upstream docs (DATA_PROCESSING.md, PUBLIC_PREVIEW.md, HOW_IT_WORKS.md) still say graph construction runs locally. Issue #673 reports the mismatch.

Implication: the deterministic code-map lane has already run on users' machines in this product. A future local or hybrid mode is a business choice, not a research problem.

## 4. Roadmap signals and what has already been proposed

No public roadmap file exists. On 4 Nov 2026 many feature and UX issues were closed as `not_planned` (#221, #251, #289, #291, #329, among others), so I can't treat closed issues as planned or rejected work. These Track 2-style proposals are **public** and I count them as crowded:

| Issue | Proposal | Overlap with my candidate space |
|---|---|---|
| #289 (closed, not planned) | Show which workflows are linked to files changed between two git revisions | diff → workflows |
| #291 (closed, not planned) | "Show what changed since the last review": new risks, fixed risks, new connections, "like checking a fitness tracker" | run-to-run diff |
| #312 (open) | `unvibecode check --staged`, a warn-only pre-commit hook with an `unvibe` alias | diff at commit time |
| #457 (open) | Workflow Scorecard graded against the 18 workflow packs, `.unvibecode/scorecard.json`, README badge, recomputed on PRs | committed state + badge |
| #476 (open) | Frictionless onboarding + CI/CD automation | CI |
| #472, #485, #576, #689 (open) | DX audits: output folder, formats, headless use, Windows | first-run friction |
| #683 (open) | PR business-impact analysis: diff → workflows, risks, checks | PR impact |
| #450 (open) | Code map hard to read on large repos | output consumption |

**Conclusion:** "diff-scoped check", "PR impact", "since last review" and "badge/scorecard" are already public, so a proposal built on any of them alone will look unoriginal. A winning entry needs a different mechanism, or has to make one of these practical in a way the public proposals don't.

## 5. Brand assets and vocabulary

- Name: **UnvibeCode**; wordmark "Unvibe**Code**" (bold split) in the report header; "⭐ Star UnvibeCode" in every report.
- Taglines: "Provide a brain for your codebase"; "Unvibe complex code. Trace what the business actually does"; "Your LLM helped write 100,000 lines of code. Now how do you understand what it actually built?"
- Output names (the brand's nouns): **Business Workflow Map**, **Connected Code Map**, **Business Risk Findings**, **Complete Repository Context**, "LLM Context", "Narrow / Optimal / Wider" context sizes.
- The verb **"unvibe"** is already used in the tagline ("Unvibe complex code"), and #312 proposes it as a CLI alias.
- Internal names that leak out: `shipreadyv2`, "ShipReady complete repository context" (in the bundle README), `shipready-api` host. These are a brand-consistency gap in the one artifact users are told to reuse.

## 6. Technical constraints that bound feasible ideas

1. **Hosted and upload-based.** Every analysis uploads source. Private-repo use needs permission. No offline mode in 0.4.0.
2. **The LLM stage costs money and can fail.** Credits were exhausted during my entire trial (and in #329 on 0.3.15). The stage is reported as non-deterministic, so anything that runs the LLM on every commit or PR multiplies cost and noise.
3. **The deterministic stage is cheap and fast.** 1.5–3.7 s server time for 38–105-file repos. Byte-identical output. Structure-only changes show up as small connection diffs (evidence §4).
4. **Language coverage is uneven.** Python and Go are good. TypeScript relative imports are mostly unresolved (2 of 49 in my test). Java gives 0 connections. Cross-service (gRPC) links are absent.
5. **Concurrency.** `/health` reports `analysis_slots: 2`. The README says "one repository at a time; if busy, retry later". A feature that fires on every commit for every user would overload this.
6. **Job IDs are bearer tokens; results are retained about 24 h.** Any shareable-link idea must avoid leaking job IDs.

## 7. What this means for Track 2

- Build the habit on the **deterministic Connected Code Map**, not on the LLM layer. It works today, costs little, gives the same answer each time, and is the output users in #291 and #289 actually valued.
- **Upload rarely, query often.** The idea should call the hosted service only when structure may have changed, and answer daily questions locally from stored output.
- **Make errors visible.** Wrong edges (Flask fixture shadowing) and gaps (TS, Java) are the biggest trust risk. Hiding them in a hairball graph doesn't fix them, so the format should put them where they get noticed and reported.
