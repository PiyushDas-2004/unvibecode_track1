# Evidence: real UnvibeCode trial (13 Nov 2026)

Everything in this proposal traces back to a file in this folder. Job IDs were removed from all logs (`<JOB_ID_REDACTED>`), because the upstream README says job IDs work as bearer tokens.

## 1. Environment

| Item | Value | Source |
|---|---|---|
| OS | Ubuntu 24.04.5 LTS, Linux 6.18 x86_64 (cloud container) | `uname -a`, `/etc/os-release` |
| Python | 3.13.18 in a fresh venv | `python --version` |
| pip | 26.2.2 (inside venv) | `pip --version` |
| UnvibeCode | **0.4.0** | `python -m unvibecode --version` |
| Install command | `python -m pip install --upgrade unvibecode` | [pip_install.log](pip_install.log) |
| Install time | 5.08 s wall | [pip_install.log](pip_install.log) |
| Wheel size | 10 kB, **zero dependencies**, 92 kB installed | `pip show -f unvibecode` |
| Warnings | none (only pip's own "new pip release" notice) | [pip_install.log](pip_install.log) |
| Package summary | "Analyze repositories using the hosted UnvibeCode engine" | wheel METADATA |
| Health | `{'status': 'ok', 'service': 'unvibecode-engine', 'busy': False, 'presentation_version': 1, 'analysis_slots': 2}` in 1.09 s | [health_direct.log](health_direct.log) |

The challenge doc was re-fetched on 13 Nov 2026 14:12 UTC ([challenge_doc_cohort3.md](challenge_doc_cohort3.md)). It matches the brief: same deadline, same Track 2 text, same 35/25/20/10/10 rubric. No discrepancies.

## 2. What 0.4.0 actually does (read from the installed client, 396 lines)

- Zips allow-listed text files, uploads them with a hard-coded public preview token to `https://shipready-api.alphashots.ai/analysis`, polls every 3 s, downloads a results ZIP, and opens the HTML report in a browser.
- CLI surface: `health`, `review --repository PATH [--dry-run] [--output DIR]`, `resume JOB_ID`. `--no-open-browser` exists but is hidden from `--help`.
- Default output folder is `./unvibecode_results` relative to the **current directory**.
- The client deliberately ignores proxy environment variables (`ProxyHandler({})`).
- No local cache, no history, no comparison between runs, no machine-readable summary on stdout.

## 3. Runs (all on 13 Nov 2026)

Wall time includes upload, polling and download. "Server" is the time UnvibeCode printed. Peak RSS is the local client only.

| # | Repository (commit) | Language | Files: dry-run / CLI says / bundle | Upload ZIP | Wall | Server | Peak RSS | Result | Log |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [pallets/flask](https://github.com/pallets/flask) `49943b5a` | Python | 140 / 105 / 102 | 194 kB | 22.8 s | 18 s | 29 MB | PARTIAL: Code Map + Context OK, Business analysis failed (API credits exhausted) | [run1_flask.log](run1_flask.log) |
| 2 | [gothinkster/node-express-realworld-example-app](https://github.com/gothinkster/node-express-realworld-example-app) `30b68e1e` | TypeScript | 57 / 38 / 38 | 113 kB | 14.0 s | 5 s | 28 MB | PARTIAL, same credits error | [run1_node-express-realworld-example-app.log](run1_node-express-realworld-example-app.log) |
| 3 | [spring-projects/spring-petclinic](https://github.com/spring-projects/spring-petclinic) `500158f7` | Java | 92 / 13 / 63 | 135 kB | 10.7 s | 3 s | 29 MB | PARTIAL: business analysis skipped, "No usable supported application connections; detected: css, html, java" | [run1_spring-petclinic.log](run1_spring-petclinic.log) |
| 4 | [GoogleCloudPlatform/microservices-demo](https://github.com/GoogleCloudPlatform/microservices-demo) `c7cb6d5b` | Go, Python, C#, Java, JS (12 services) | 273 / 63 / 74 | 461 kB | 25.6 s | 18 s | 30 MB | PARTIAL, same credits error | [run1_microservices-demo.log](run1_microservices-demo.log) |
| 5 | Flask `49943b5a` again, run from inside the repo with default output | Python | same | same | 22.5 s | 14 s | 29 MB | PARTIAL, credits error; left untracked `unvibecode_results/` in the repo | [run2_flask_same_commit_default_output.log](run2_flask_same_commit_default_output.log) |
| 6–9 | Flask at 4 older commits (see [flask_snapshot_commits.txt](flask_snapshot_commits.txt)) | Python | 105 each | – | 18.1–26.2 s | 13–19 s | 29–30 MB | PARTIAL, credits error | `run_flask_*.log` |

Exact command for every run: `python -m unvibecode review --repository <path> --output <dir> --no-open-browser`, wrapped by [tools/measure.py](tools/measure.py) for timing and memory.

No API key or account was needed. Network access was required for every run. Every run uploaded the whole repository again.

### The hosted LLM stage was down for the whole trial

All runs that reached business analysis stopped at STEP_03. The status file says `RateLimitError: Error code: 429 ... 'code': 'credit_balance_exhausted'` from the model provider ([raw_outputs/flask/analysis-status.json](raw_outputs/flask/analysis-status.json)). So **Business Workflow Map and Business Risk Findings were never produced in my trial.** Upstream issue #329 (closed as not planned on 4 Nov) reports the same failure on 0.3.15, and #291's author says this failure is why they had "no clear reason to open the tool again".

I retried at 14:46 UTC (`run_flask_retry_llm.log`) and at 15:48 UTC (`run_flask_retry2_llm.log`) and got the same error. That makes **10 of 10** runs that reached business analysis. For a real Business Workflow Map, the prototype uses UnvibeCode's own published django-payments sample, verified against the matching commit ([business_reach_verification.md](business_reach_verification.md)).

The deterministic "fast lane" (Connected Code Map + Complete Repository Context) **succeeded on all 9 runs**, taking 1.5–3.7 s of server time (`FAST_LANE.duration_seconds` in each `analysis-status.json`).

## 4. Repeat-run behaviour (day-2 test)

| Question | Observation | Evidence |
|---|---|---|
| Is a second run cached? | No. Same upload, same wait (14 s vs 18 s server). | runs 1 and 5 |
| Is it deterministic? | **Yes for the code-map lane.** `manifest.json`, `chunks.jsonl`, `connections.jsonl`, `selections.jsonl`, `unresolved_relationships.jsonl` and the graph data `fast_lane_context_store.js` were byte-identical between runs 1 and 5 (`cmp`, md5 `f3155581...`). | run 1 vs run 5 |
| Where does output go? | A new timestamped folder every run, e.g. `flask-unvibecode-analysis-20261113_141453/`. Nothing links run 2 to run 1. | output listings in `raw_outputs/*/output_file_listing.tsv` |
| Does it touch my repo? | Running from the repo root with the default `--output` left `?? unvibecode_results/` in `git status`. | run 5 |
| Can two snapshots be compared? | Not by the tool. I compared them myself (below). | – |

### Are chunk IDs stable across commits?

No. Between Flask `3596b1ab` and `d73fa1cd` (a 19-line change in 6 files), 97 of 481 chunk IDs changed, 91 of them in `tests/test_basic.py`, because inserting lines shifts later functions. Chunk IDs encode position, not content. Files whose content changed without shifting lines (`app.py`, `helpers.py`) kept their chunk IDs.

### Is the file-and-symbol connection set stable across commits?

Yes, and it moves only when structure moves. Comparing connections as (source file, target file, symbol), ignoring line numbers:

| Snapshot pair | Code change | Connection changes |
|---|---|---|
| `3596b1ab` → `d73fa1cd` | 6 files, +19/-7 lines (new `app.query` decorator) | **0 added, 0 removed** |
| `d73fa1cd` → `49943b5a` (HEAD) | Python 3.10 drop, werkzeug 3.2 compat (external imports only) | **0 added, 0 removed** |
| `33012325` → `c2705ffd` ("merge app and request context", 1 refactor commit) | large refactor of `ctx.py`, `app.py` | **3 added, 2 removed** |

The 5 changes in the refactor, checked against the source:

- `- src/flask/app.py → src/flask/ctx.py · RequestContext`: correct. The parent commit has `from .ctx import RequestContext` (app.py:32); the refactor removed it.
- `- src/flask/app.py → src/flask/sansio/scaffold.py`: correct. The parent has `from .sansio.scaffold import _sentinel` (app.py:45); the refactor removed it.
- `+ src/flask/helpers.py → tests/conftest.py · app_ctx`: **wrong**. helpers.py:17 is `from .globals import app_ctx`. The engine matched it to the `app_ctx` pytest fixture in `tests/conftest.py:55`.
- `+ tests/test_reqctx.py → tests/conftest.py · app_ctx` and `+ tests/test_session_interface.py → tests/conftest.py · app_ctx`: plausible. Tests take the `app_ctx` fixture by parameter name.

## 5. Accuracy checks against source

**Correct (Python, Flask HEAD).** I picked 6 random symbol connections (seed 7) and checked them. All 6 point at the right definition: `_split_blueprint_path` (helpers.py:645), `Flask` (app.py:108), `Request` (wrappers.py:18), `JSONTag` (json/tag.py:60), `after_this_request` (ctx.py:118), `jsonify` (json/__init__.py:138). Reported target lines point at the start of the chunk, which can be a few lines before the `def` (642 vs 645, 106 vs 108, 116 vs 118). `cli.py → helpers.py · get_debug_flag/get_load_dotenv` matches cli.py:24-25.

**Wrong: module shadowing (Flask).** 58 connections from 43 test and example files that do `import flask` / `from flask import ...` point to `tests/test_apps/cliapp/inner1/inner2/flask.py`, a 3-line test fixture. **0** connections point to `src/flask/__init__.py`. That fixture becomes the most-connected file in the map, and the map's file picker lists it first ([screenshots/flask_connected_code.png](screenshots/flask_connected_code.png)).

**Wrong: external modules matched to local test files (found by the prototype's "Check these connections" section, then verified).** At Flask `c2705ffd`, `src/flask/app.py`, `cli.py`, `ctx.py`, `testing.py` and `typing.py` get `file_import` connections (confidence `medium`) to `tests/test_apps/helloworld/wsgi.py`, whose whole content is `from hello import app`. The real imports are external, e.g. `from werkzeug.wsgi import get_host` (app.py:27) and `from _typeshed.wsgi import ...`. `src/flask/testing.py` is also connected to `tests/test_apps/blueprintapp/apps/admin/static/css/test.css`. Medium-confidence edges are not uniformly wrong: `examples/tutorial/flaskr/__init__.py → src/flask/app.py · Flask` is medium and correct. So filtering by confidence alone would drop good edges.

*Upstream already tracks this class of error:* #366 ("imports resolve to unrelated same-name files in tests/"), #425 (absolute imports falling back to a file-stem match) and #707 (false import edges through `stem_fallback`) are open. So these are known engine limits, not new bugs. That is one more reason to show them in a reviewable section instead of hiding them in a graph.

**Thin: TypeScript relative imports.** In node-express-realworld, `src/` has 49 relative imports (`grep "from '\.{1,2}/"`). The bundle has **2** connections. `./article.service` and `../auth/auth` are listed in `unresolved_relationships.jsonl` with reason `module_scope_mismatch`, even though the correct candidate file is named in the same record.

**Missing: Java.** spring-petclinic: 63 files, 1,558 code sections, **0** cross-file connections. Business analysis was skipped for this reason. Java is not in the README's language table either.

**Mixed: multi-service (microservices-demo).** 86 connections, all inside Go (78) and JS (8) services. Sampled Go targets are correct (`getProduct` → frontend/rpc.go:51, `getRecommendations` → rpc.go:99, `IsNegative` → money.go:56). Reported source lines (210, 319) do not match the call sites (154, 178, 225, 266). Python services that use sibling imports (`emailservice`: `import demo_pb2`, `from logger import ...`) have 0 connections. There are no service-to-service (gRPC) connections, so the map does not show how the 12 services talk to each other.

**Takeaway.** The file/symbol graph is fast, deterministic and mostly right for Python and Go. It is incomplete for TypeScript and missing for Java. It has a few systematic false edges. The LLM layer was unavailable, and upstream issues #408, #516 and #251 report that it gives different workflow sets on repeated runs of unchanged code. **A daily habit should rest on the deterministic layer, and it should show its errors where people can see and report them.**

## 6. What the user sees

- [screenshots/flask_full_report.png](screenshots/flask_full_report.png): the landing page says PARTIAL, has two tabs (Connected Code, LLM Context) and an interactive graph of all files.
- [screenshots/flask_connected_code.png](screenshots/flask_connected_code.png): the graph view. Hundreds of nodes, no question answered until you click a file.
- The terminal prints a summary and file paths, and nothing that answers a question about the code.

## 7. Upstream research artifacts

- [upstream_issues_index.tsv](upstream_issues_index.tsv): all 650 issues (number, state, date, title, labels) from the GitHub search API, 13 Nov 2026.
- [upstream_pull-requests_index.tsv](upstream_pull-requests_index.tsv): all 110 PRs.
- Upstream clone examined at `c75b75e2` (4 Nov 2026), license Apache-2.0 plus proprietary package components ([docs/LICENSE_CLARIFICATION.md](https://github.com/FinanceFlash/unvibecode/blob/main/docs/LICENSE_CLARIFICATION.md)). No upstream code is copied into this repository.
