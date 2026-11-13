# Pass 3: second red team, steal-from-yourself check, convergence

**Inputs re-read:** the ledger (212 rows), the pass-2 revision, redteam.md round 1, and the friction log entries on trust (F08, F09, F10).
**Added:** 3 problems (P101–P103) and 3 solutions (S113–S115), all from attacking K1b.

## New problems found by attacking the leader
- **P101.** A committed file containing wrong edges looks authoritative. On Flask today, 58 connections would point to a 3-line fixture. → **S113:** a "Check these connections" section for suspicious edges (non-test → `tests/`, files that shadow a package name such as `flask.py` outside `src/`). It turns an engine error into a visible, reportable line instead of a silent one.
- **P102.** Some teams forbid generated files in git. → **S114:** a `--no-commit` mode keeps the baseline in the CI cache or an artifact and still reports deltas. It loses git history and filename brand recall, so it is the fallback, not the default.
- **P103.** A map that is only useful once history builds up gives no day-1 reason to adopt it. → **S115:** the first render already gives an onboarding page: hub files ranked by direct importers, and area-to-area dependencies. Reading it costs a teammate nothing and needs no upload permission.

## New or variant concepts scored
| ID | Concept | R | W | F | B | O | Total |
|---|---|---|---|---|---|---|---|
| K21 | K1b in no-commit mode only | 24 | 20 | 17 | 5 | 7 | 73 |
| K22 | K2 PR bot rebuilt on the K1b engine (comment instead of job summary) | 27 | 20 | 16 | 9 | 5 | 77 |
| K23 | K6 AI-session impact as a stand-alone product | 23 | 18 | 13 | 6 | 7 | 67 |

K22 is the closest challenger, at 7 points behind. It scores lower on originality and adds the PR-comment noise the jaded-engineer persona objects to. K1b keeps an **opt-in** comment mode for teams that want one, so there's nothing to merge.

## Steal-from-yourself check
**Would 3 other competent Claude users land on the same core?**

- "Generate an ARCHITECTURE.md": **likely** (crowdedness 5, C25). Usually proposed without a freshness mechanism, delta reporting, or data on stability.
- "Diff-scoped pre-commit / PR impact": **already public** (#312, #683).
- **"Commit the deterministic code map as a line-free baseline, gate uploads on import-line changes, report only new connections (freeze), and let git blame be the architecture history":** I don't expect three people to land on this. The pieces that make it hard to copy all come from my trial: chunk IDs are unstable (97 changed) while the file+symbol keys are stable (0 changes); churn was measured at 6–37%; the LLM was down; transitive closure saturates on Flask.

To make it **more** distinctive without losing rubric points, the submission will:
1. Lead with the **lockfile analogy and the filename** `UNVIBECODE.md`, which is concrete and memorable.
2. Quote the measured stability numbers and the refactor delta (`+3/-2` on Flask `c2705ff`).
3. Show the "Check these connections" section catching a real engine error. The prototype does this on Flask.

## Convergence check
| Criterion | Status |
|---|---|
| (a) at least 3 passes | 3 done |
| (b) last two passes added no candidate within 5 points of the leader | Pass 2 best new: K19 at 70 vs 84. Pass 3 best new: K22 at 77 vs 84. Both more than 5 behind. |
| (c) leader survived the red team intact | K1b survived round 2 with three additions (S113–S115) and no change to its core loop. See redteam.md. |

**Converged after pass 3.** Leader: **K1b, the committed, self-checking UnvibeCode map file (`UNVIBECODE.md`).**

## Remaining uncertainty
- Trigger frequency on low-churn repos stays low for the structural delta (0.1 a week on Flask). The per-PR reach line covers this, but its usefulness on small PRs is a hypothesis that needs testing.
- Brand recall through a filename is reasoned by analogy (`yarn.lock`, `CODEOWNERS`), not measured for UnvibeCode.
- Coverage limits (TS, Java) mean the first cohort should be Python and Go repos.
