# Where every example came from

All examples were produced on 13 Nov 2026 (re-rendered after pass 4 from the same bundles, which are kept as fixtures) with `unvibecode==0.4.0` (hosted engine) and `unvibecode-mapfile 0.1.0` on Ubuntu 24.04, Python 3.13. `build` and `check` with an upload made live calls to the UnvibeCode service. `impact` and gate-skipped `check` runs made none.

| Folder | Repository | Commit(s) | What it shows |
|---|---|---|---|
| `django-payments/` | https://github.com/jazzband/django-payments | map at `5607e9e88762df9831980832c194f49b227dbe93` (18 Oct 2026); tested on the 8 commits up to `47449a1516772e3996060d77efa1ab970ad0dcd1` | `UNVIBECODE.md` with the Business Workflow index. The code map is from a live run; the workflows are from UnvibeCode's **published** Business Workflow Map sample for this repo, because the hosted LLM stage was out of credits on all my runs. `after_18_oct_log.txt`: one-line check titles for every later commit. `unvibe_uncommitted_log.txt`: `unvibe` on PR #501's diff applied but not committed (76 ms). |
| `flask/` | https://github.com/pallets/flask | `49943b5a94413a530761350f04e896f76e8d620e` | Day-1 map: hubs, area connections, 18 flagged suspicious connections (incl. the `flask.py` fixture shadowing), full connection list. `rebuild_log.txt`: second run → "Unchanged". |
| `flask-refactor-c2705ff/` | https://github.com/pallets/flask | before `330123258e8c3dc391cbe55ab1ed94891ca83af3`, after `c2705ffd9ce1dc8476cb29eaf5ff5d4c719852d9` ("merge app and request context") | `check` finds +3/-2 connections; `impact` lists hubs and symbol users in 91 ms without uploading; `git_style_diff.txt` is what a reviewer sees in the PR: 30 diff lines for a 36-file refactor. The `# UnvibeCode Map:` title differs only because the two snapshots were separate folders. |
| `flask-gate/` | https://github.com/pallets/flask | A: `3596b1ab...` → `d73fa1cd...`; B: `d318b68` | A: import lines changed in a test → upload → "No structural change". B: no import line changed → upload skipped (70 ms) and reach report in 68 ms. |
| `microservices-demo/` | https://github.com/GoogleCloudPlatform/microservices-demo | `c7cb6d5bfd6ea3aed768634ebbcb98cb7a523712` | Multi-service repo: 17 connected file pairs, all inside single services; coverage section shows 22 of 74 files connected. |
| `node-express-realworld/` | https://github.com/gothinkster/node-express-realworld-example-app | `30b68e1e881462b2f4164ea09ab4c4f5699c7b0b` | TypeScript coverage gap made visible: 2 connections, 49 unresolved relative imports, "Sparse map" warning. |

The test fixtures in `../fixtures/` are the same real bundles with source text removed (see `FIXTURE_NOTE.txt` inside each ZIP).
