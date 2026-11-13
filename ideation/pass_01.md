# Pass 1: broad enumeration and first scoring

**Inputs re-read:** friction_log.md (22 entries), user_journey.md, upstream_audit.md, crowded_ideas.md.
**Added:** 88 problems/triggers (P001–P088, T031–T064) across all 12 lenses, and 100 solutions (S001–S100), 5 for each of the top 20 problems/triggers.

## Top 20 problems/triggers chosen for solution generation
T035 PR review · T046 after `git pull` · T047 after an AI change · T034 PR authoring · T033 onboarding · T036 debugging · T031 starting a ticket · T045 docs drift · T037 dependency upgrade · P024 no memory · P026 no diff · P017 graph-only output · P065 single-player · P069 no trigger · P071 no investment · P073 brand absent · P076 false edges · P008 private upload · P081 LLM cost · T064 AI prompt context.

Selection rule: severity H or a weekly-or-more frequency, plus evidence beyond "hypothesis" where available.

## Concepts assembled from the 100 solutions
Solutions were grouped into concepts only when they serve one loop (trigger → value → artifact → exposure → next trigger).

| ID | Concept | Built from | Crowdedness |
|---|---|---|---|
| K1 | **Committed map file**: the deterministic Connected Code Map written as a line-free text file in the repo (lockfile-style), refreshed by a command, checked in CI, its diff visible in PRs, its git history = architecture history, local queries offline | S002, S007, S020, S021, S036, S047, S062, S066, S071, S076, S081, S086 | 3 |
| K2 | GitHub Action PR comment (hosted run per PR) | S001, S017, S067 | 9 |
| K3 | Pre-commit `check --staged` | S011 (partly), #312 | 8 |
| K4 | "Since last review" run-to-run diff | S046, S051, #291 | 8 |
| K5 | post-merge catch-up briefing | S006, S008 | 3 |
| K6 | AI-session impact block (agent hook prints a branded impact block after an assistant edits code) | S011, S012, S014 | 4 |
| K7 | `unvibe ctx` branded context pack for AI chats | S096, S097 | 5 |
| K8 | Stack-trace mapper | S026, S029 | 3 |
| K9 | VS Code extension | S010, S019, S035 | 9 |
| K10 | Onboarding tour / flashcards | S022, S024 | 4 |
| K11 | Workflow scorecard + badge | S040, S079, #457 | 8 |
| K12 | Weekly scheduled bot PR refreshing an architecture doc | S037 | 4 |
| K13 | Slack/Teams digest | S009, S068 | 7 |
| K14 | Dependency-upgrade usage finder | S041, S042 | 3 |
| K15 | Architecture rules enforced from the map (import-linter style) | S073, S015 | 3 |
| K16 | AGENTS.md / CLAUDE.md section generated from the map | S098 | 3 |

## Pass-1 scores (detail in scoring/rubric_matrix.md)

| Rank | Concept | R/35 | W/25 | F/20 | B/10 | O/10 | Total |
|---|---|---|---|---|---|---|---|
| 1 | K1 committed map file | 26 | 19 | 17 | 9 | 9 | **80** |
| 2 | K6 AI-session impact block | 24 | 19 | 14 | 6 | 7 | 70 |
| 3 | K15 architecture rules | 23 | 17 | 15 | 7 | 7 | 69 |
| 4 | K2 PR comment bot | 24 | 20 | 13 | 8 | 3 | 68 |
| 5 | K7 branded context pack | 20 | 18 | 17 | 6 | 4 | 65 |
| 6 | K16 AGENTS.md section | 18 | 16 | 18 | 5 | 7 | 64 |
| 7 | K5 post-merge catch-up | 22 | 17 | 12 | 6 | 6 | 63 |
| 7 | K12 weekly bot PR | 17 | 15 | 16 | 9 | 6 | 63 |
| 9 | K9 VS Code extension | 22 | 21 | 10 | 7 | 2 | 62 |
| 10 | K3 pre-commit check | 22 | 17 | 10 | 6 | 3 | 58 |
| 11 | K14 dependency finder | 14 | 14 | 17 | 5 | 6 | 56 |
| 12 | K8 stack-trace mapper | 15 | 14 | 14 | 5 | 6 | 54 |
| 13 | K4 since-last diff | 18 | 12 | 15 | 5 | 3 | 53 |
| 14 | K10 onboarding tour | 12 | 9 | 15 | 6 | 7 | 49 |
| 14 | K13 Slack digest | 15 | 12 | 13 | 7 | 2 | 49 |
| 16 | K11 scorecard badge | 14 | 8 | 9 | 9 | 3 | 43 |

## Red team, pass 1 (summary; full text in redteam.md)
- **K1 leads but has a hole.** Measured import churn (evidence/import_churn.txt) is 0.1 structural commits a week on Flask, 0.7 on healthchecks and 9.0 on netbox. On mature repos the map rarely changes, so "the map changed" alone is a weak weekly trigger. **Fix for pass 2:** every PR needs some value, not only structural PRs.
- **K6 and K15 are not stand-alone products.** They need a stored map to read from. K6 without one means a hosted upload after every AI session. K15 needs someone to write rules, which is friction. **Both are better as features that read K1's file.**
- **K2** depends on a hosted run (and the LLM for "impact") on every PR push. In my trial the LLM was down and the service has 2 slots. It is the most-proposed idea.

## What changed in this pass
First full ledger and first ranking. The leader is K1. Next pass: fix K1's trigger frequency, and look for new triggers through analogies from outside developer tools.
