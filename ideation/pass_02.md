# Pass 2: under-covered lenses, outside analogies, revision of the leader

**Inputs re-read:** the ledger (188 rows), friction_log.md, pass-1 red team, and the finished competitor_landscape.md.
**Added:** 12 problems/triggers (P089–P100) and 12 solutions (S101–S112).

## Lenses that pass 1 under-covered, and analogies used
| Analogy (outside or adjacent) | What it suggested | Ledger rows |
|---|---|---|
| Bank statement / returning from holiday | "What changed while I was away?" is a monthly moment for everyone | P089, S106 |
| Codecov patch coverage, Sonar "new code" gate | Report only the **delta a PR introduces**, never the whole state | P090, P098, S101 |
| ArchUnit `FreezingArchRule` (verified: archunit.org user guide) | Commit today's state as a baseline; report only new violations; **line numbers ignored by default** | P094, S104 |
| Lockfiles (`npm ci`, `uv lock --check`, `go mod tidy -diff`) | A committed generated file plus a CI freshness check makes regeneration a normal part of a PR | P099, S036 |
| CODEOWNERS | Who should review = who owns the **dependents**, not the folder | P091, S110 |
| OSS maintainers flooded with AI-generated PRs | A label for "reaches into core hubs" helps triage | P095, S103 |
| `git blame` | Commit the map and git becomes the history store for free | P096, S105 |
| Test-impact tools (pytest-testmon, `nx affected`) | Select tests from the map | P092, S107 |
| Agents read AGENTS.md every session | Point the agent at the map | P093, S108 |
| GitHub code search counts of `yarn.lock` | Count committed map files to measure retained adoption without telemetry | P100, S111 |
| Capacity data (my churn measurement) | Upload only when an import line changed | P097, S109 |

## New concepts this pass
| ID | Concept | R | W | F | B | O | Total | Note |
|---|---|---|---|---|---|---|---|---|
| K17 | Return-from-leave summary | 13 | 13 | 17 | 6 | 6 | 55 | A side effect of K1's history; too rare to stand alone |
| K18 | Reviewer suggestion from dependents' owners | 15 | 15 | 12 | 4 | 7 | 53 | Needs ownership data |
| K19 | Maintainer triage label "touches hub" | 21 | 18 | 17 | 6 | 8 | 70 | Good per-PR value; needs a stored map |
| K20 | Affected-tests from the map | 27 → **18** | 21 → 15 | 13 → 10 | 6 | 7 | 74 → **56** | **Demoted by evidence:** on Flask the transitive closure from `app.py`, `helpers.py` and `scaffold.py` reaches all 74 dependents (evidence/affected_tests_closure.txt). On hub-heavy repos it selects nearly everything, and the fixture-shadowing bug would route test edges wrongly. |

No new concept came within 5 points of the leader (K1b = 84 below).

## Revision of the leader: K1 → K1b
The pass-1 red team found that K1 fires rarely on mature repos. Pass 2 fixes this **inside the same loop**, without adding new channels:

1. **Every PR gets a reach line, computed locally from the committed file with zero uploads.** "This PR changes 3 files; 42 files import them directly; hub touched: `src/flask/app.py` (25 direct importers)." Direct (1-hop) dependents only, because transitive closure saturates (K20 evidence). This also covers K19's triage value.
2. **Freeze semantics (ArchUnit).** The CI check reports only connections the PR **adds or removes**, keyed by file + symbol with no line numbers. My trial shows that key is stable: 0 changes across two non-structural commit ranges, 5 changes on a real refactor.
3. **Upload gate.** CI calls the hosted service only if the diff changes an import line. Measured share of commits that do: 6% (Flask), 8% (healthchecks), 37% (netbox).
4. **Errors become visible.** The file has a "Check these connections" section listing suspicious edges, such as non-test code pointing into `tests/` (this would have caught Flask's `helpers.py → tests/conftest.py`).
5. **The AI-session moment (K6) and AGENTS.md (K16) read the same file.** `impact` runs on the working tree after an assistant edits code, with no upload.

| Concept | R | W | F | B | O | Total |
|---|---|---|---|---|---|---|
| **K1b** committed, self-checking map file | 29 | 21 | 17 | 9 | 8 | **84** |

Originality drops one point versus K1 because "PR reach" overlaps #683 in surface. The mechanism differs: local, no LLM, no per-PR upload. Repeat usage rises 3 points because every PR now triggers it.

## What changed in this pass
- +12 problems, +12 solutions, +4 concepts.
- Leader revised from K1 (80) to K1b (84). Runner-ups unchanged except K19 (70, folded into K1b) and K20 (demoted to 56 on evidence).
- One idea was killed by measurement rather than opinion (K20).
