# Pass 5: searching for anything better than the new leader (A+B)

**Inputs re-read:** pass_04.md, the brief, evidence/business_reach_verification.md, and the redteam rounds 1–2.
**New lens:** "deliberate, named invocation" (the brief's main objection to MCP), plus analogies from git's own extension model, shell prompts, commit metadata and standups.

| ID | Candidate | R | W | F | B | O | Total | Note |
|---|---|---|---|---|---|---|---|---|
| P5a | `git unvibe`: git runs any `git-<name>` executable on PATH, so installing `git-unvibe` makes the brand a git subcommand with no config | – | – | – | – | – | – | **Folded into A+B** as a second spelling of the same command. Zero cost, and it fits the git habit developers already have. |
| P5b | Shell-prompt segment ("unvibe: 2 workflows") whenever the working tree touches a workflow | 25 | 18 | 16 | 9 | 6 | 74 | Ambient but noisy; prompt latency matters on every keypress |
| P5c | `prepare-commit-msg` hook adds a trailer `Unvibe-Workflows: Stripe checkout`, so `git log --grep` becomes a business search | 27 | 19 | 18 | 10 | 8 | 82 → **78** after red team | Jaded engineer: tools that edit commit messages get uninstalled. Also it's automation again, not a deliberate return (gap G1). |
| P5d | Weekly "workflow changelog" for standup and release notes, from PR check titles | 23 | 18 | 17 | 9 | 7 | 74 | A nice consumer of A+B data; weekly, not daily |
| P5e | VS Code status bar / CodeLens reading UNVIBECODE.md | 26 | 22 | 12 | 9 | 6 | 75 | Most-proposed channel; can come later on the same file |
| P5f | Use the 18 workflow packs (upstream `prebuilt-workflow-paths/`) as checklists when a PR touches a matching workflow | 22 | 16 | 12 | 8 | 7 | 65 | Needs workflow-to-pack matching; already proposed in #457 |

**Best new candidate: P5c at 78**, 10 points behind A+B (88). Nothing came within 5 points.

## Steal-from-yourself check on A+B
- "Show business workflows a PR touches": **public** as #683 (via an LLM per PR) and #289. Surface overlap: yes.
- "`unvibe` alias": **public** in #312 (for a pre-commit hook that uploads).
- What A+B adds that none of them has:
  1. A **committed, line-free workflow index**. Workflows are refreshed on purpose, so per-change answers need no LLM and no upload. It is kept when the LLM stage fails, which was the observed state on 10/10 runs.
  2. **Exact enclosing-definition matching**, verified 8/8 on real post-sample django-payments commits after two bug fixes found by hand.
  3. **The same line in two places.** The author sees it when they deliberately type `unvibe`; the reviewer sees it in a quiet check-run title. Neither is a bot comment.
  4. The brand is carried by UnvibeCode's **own vocabulary** (workflow names) rather than a generic graph.

Three people given the brief could plausibly land on "PR impact in business terms". It's much less likely they'd land on "a committed workflow index looked up locally, with a deliberate named command and a quiet check title, verified on real later commits".

## Convergence
Passes 4 and 5 are done. Pass 5 added nothing within 5 points of the leader. The leader survived red-team round 3 (redteam.md). **Converged: A+B is the final recommendation.**
