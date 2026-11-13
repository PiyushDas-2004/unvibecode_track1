# Rubric matrix (final scores after pass 3)

Official Track 2 rubric: **R** = likelihood of real repeat usage (35), **W** = fit with everyday workflows and ease of access (25), **F** = feasibility and specificity (20), **B** = visible recall / brand attribution (10), **O** = original reasoning (10).
Extra columns (not in the rubric): **Crowd** = crowdedness 1–10 (lower is better); **Ev** = how much of the case rests on my verified trial (H/M/L).
Evidence references: `E§n` = evidence/README.md section n; `churn` = evidence/import_churn.txt; `CL` = research/competitor_landscape.md.

## Final ranking (after passes 4–5: brief re-read phrase by phrase)

Pass 4 re-graded every finalist against the brief's own words, not only the rubric. The brief says MCP fails because users "benefit … without remembering its name or deliberately returning to it", and it asks for UnvibeCode to be "memorable as a product". Under that reading, the pass-3 leader K1b (a generic import-graph file whose value arrives through CI) drops from 84 to 80.

| Rank | ID | Concept | R | W | F | B | O | Total | Crowd | Ev |
|---|---|---|---|---|---|---|---|---|---|---|
| **1** | **A+B** | **Committed UnvibeCode map with a Business Workflow index; opened deliberately with `unvibe` / `git unvibe`; the same line shown as a quiet PR check title** | **31** | **22** | **16** | **10** | **9** | **88** | 3 | H |
| 2 | A | Business Workflow index + PR check only (no deliberate command) | 29 | 21 | 16 | 10 | 9 | 85 | 3 | H |
| 3 | K1b / v1 | Import-graph lockfile + CI summary (pass-3 leader, re-scored) | 27 | 21 | 17 | 7 | 8 | 80 | 3 | H |
| 4 | B | `unvibe` command alone | 27 | 20 | 16 | 9 | 7 | 79 | 5 | M |
| 5 | P5c | Commit-trailer `Unvibe-Workflows:` | 26 | 18 | 18 | 9 | 7 | 78 | 2 | M |
| 6 | K22 | PR comment bot on the K1b engine | 27 | 20 | 16 | 9 | 5 | 77 | 7 | H |
| 7 | E / P5e | VS Code CodeLens / status bar | 26 | 22 | 12 | 9 | 6 | 75 | 8 | L |
| 8 | P5b, P5d | Prompt segment; weekly workflow changelog | – | – | – | – | – | 74 | 3 | L |
| 9 | C, D | URL-swap web page; assistant-only `/unvibe` | – | – | – | – | – | 70 | 6–7 | L |

### Justification for A+B (88)
- **R 31/35.** There are two triggers. The developer's own deliberate moment is "an AI assistant or I just changed code; what business flow did that touch?" Typing `unvibe` answers it in about 0.1 s, offline. The reviewer's moment is every PR, where the same line appears as the check title. Value builds up because the index and map live in git. The brief's two failure modes are covered: the user types the name, and the user returns on purpose. I hold back 4 points because daily manual use is a hypothesis; the experiment measures it separately from CI runs.
- **W 22/25.** Terminal, git and the PR checks list are the most-used developer surfaces. An individual needs one `build` and can then use `unvibe` with no CI. Teams add one workflow file. It loses points for the one hosted run and an upload approval.
- **F 16/20.** Verified end to end. The workflow index is parsed from UnvibeCode's own Business Workflow Map page (django-payments sample, 6/6 references matched). The matcher is correct on 8/8 real later commits after two fixes. There are 38 tests. It loses points because the workflow refresh needs the hosted LLM stage, which was down for my whole trial (mitigated by keeping the last index), and because Python is precise while other languages use a weaker fallback.
- **B 10/10.** The name is typed (`unvibe`) and shown in the PR checks list ("UnvibeCode · 1 business workflow(s): provider-backed payment checkout…"). The artifact sits next to README.md. Most of all, what people remember is UnvibeCode's own noun, the **business workflow**, which no import-graph tool can produce.
- **O 9/10.** The mechanism comes from trial evidence: line-free keys proven stable, LLM kept out of the per-change loop, kept-on-failure, enclosing-scope matching verified on real later commits. It drops one point for surface overlap with #683 and #312.

---

## Pass 1–3 ranking (superseded by the table above; kept for the audit trail)


| Rank | ID | Concept | R | W | F | B | O | Total | Crowd | Ev |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | K1b | Committed, self-checking UnvibeCode map file (`UNVIBECODE.md`) | 29 | 21 | 17 | 9 | 8 | **84** | 3 | H |
| 2 | K22 | PR comment bot rebuilt on the K1b engine | 27 | 20 | 16 | 9 | 5 | 77 | 7 | H |
| 3 | K21 | K1b, no-commit mode only | 24 | 20 | 17 | 5 | 7 | 73 | 3 | H |
| 4 | K6 | AI-session impact block (stand-alone, pass 1) | 24 | 19 | 14 | 6 | 7 | 70 | 4 | M |
| 4 | K19 | Maintainer triage label "touches hub" | 21 | 18 | 17 | 6 | 8 | 70 | 2 | M |
| 6 | K15 | Architecture rules from the map | 23 | 17 | 15 | 7 | 7 | 69 | 3 | M |
| 7 | K2 | PR comment bot, hosted run per PR | 24 | 20 | 13 | 8 | 3 | 68 | 9 | H |
| 8 | K7 | Branded context pack for AI chats | 20 | 18 | 17 | 6 | 4 | 65 | 5 | M |
| 9 | K16 | AGENTS.md section from the map | 18 | 16 | 18 | 5 | 7 | 64 | 3 | L |
| 10 | K5 | post-merge catch-up briefing | 22 | 17 | 12 | 6 | 6 | 63 | 3 | M |
| 10 | K12 | Weekly scheduled bot PR | 17 | 15 | 16 | 9 | 6 | 63 | 4 | M |
| 12 | K9 | VS Code extension | 22 | 21 | 10 | 7 | 2 | 62 | 9 | L |
| 13 | K3 | Pre-commit `check --staged` (#312) | 22 | 17 | 10 | 6 | 3 | 58 | 8 | M |
| 14 | K14 | Dependency-upgrade usage finder | 14 | 14 | 17 | 5 | 6 | 56 | 3 | M |
| 14 | K20 | Affected tests from the map | 18 | 15 | 10 | 6 | 7 | 56 | 2 | H (negative) |
| 16 | K17 | Return-from-leave summary | 13 | 13 | 17 | 6 | 6 | 55 | 3 | M |
| 17 | K8 | Stack-trace mapper | 15 | 14 | 14 | 5 | 6 | 54 | 3 | L |
| 18 | K4 | Since-last-review diff (#291) | 18 | 12 | 15 | 5 | 3 | 53 | 8 | M |
| 18 | K18 | Reviewer suggestion from dependents' owners | 15 | 15 | 12 | 4 | 7 | 53 | 3 | L |
| 20 | K10 | Onboarding tour / flashcards | 12 | 9 | 15 | 6 | 7 | 49 | 4 | L |
| 20 | K13 | Slack/Teams digest | 15 | 12 | 13 | 7 | 2 | 49 | 7 | L |
| 22 | K11 | Workflow scorecard + badge (#457) | 14 | 8 | 9 | 9 | 3 | 43 | 8 | M |

Tie-break rule: within 5 points, prefer lower crowdedness, then higher evidence strength. No tie-break was needed at the top: K1b leads K22 by 7.

---

## Justifications (serious candidates)

### K1b: committed, self-checking UnvibeCode map file (84)
- **R 29/35.** Triggers come from events that already happen: every PR gets a locally computed reach line; structural PRs (measured 6% of Flask, 8% of healthchecks and 37% of netbox commits, `churn`) get a freeze delta that asks for a refresh, like a stale lockfile; teammates and AI agents open the file to orient themselves. It loses points because on low-churn repos the structural trigger is rare (0.1 a week on Flask), and the value of the per-PR reach line on small PRs is untested.
- **W 21/25.** It lives in the places a team already works (the repo tree, PR "Files changed", CI job summary, `git log`) and adds no new app. Reading the file needs no install and no upload permission. It loses points for CI setup and the one-time approval for uploading in CI.
- **F 17/20.** v0 is a thin layer over the existing deterministic context ZIP, and my prototype was built on real bundles. Determinism is verified (byte-identical runs, E§4), and so is key stability (0 connection changes over two non-structural ranges, +3/−2 on a real refactor, E§4). It loses points because TS/Java coverage is thin (E§5), the refresh step still needs the hosted service, and an ideal `unvibecode map` subcommand would need upstream work.
- **B 9/10.** The filename `UNVIBECODE.md` sits next to README.md in every clone, appears in PR diffs and `git log`, and names the tool in its header and in the CI check name. This is the same mechanism that put "yarn" and "poetry" into every repo listing (`CL`). It's held back from 10 because recall through a filename isn't measured for UnvibeCode yet.
- **O 8/10.** The specific mechanism comes from trial evidence nobody else has published: chunk IDs are unstable but file+symbol keys are stable, upload gating uses measured churn, freeze semantics avoid noise, and suspicious edges are shown openly. It drops 2 because "PR impact" (#683) and "architecture doc" ideas share the same surface.
- **Crowd 3, Ev H.**

### K22: PR comment bot on the K1b engine (77)
- **R 27.** Fully automatic on every PR. **W 20.** Lives in the PR. **F 16.** Same engine as K1b, plus a GitHub App/token to post comments. **B 9.** A comment on every PR names the tool. **O 5.** The comment surface is the most-proposed channel (#476, #683), and per-PR comments draw the noise objection (redteam round 1). Offered inside K1b as opt-in, not the default.

### K21: no-commit mode only (73)
- **R 24.** Same triggers, but no shared file for teammates or agents to open. **W 20.** CI only. **F 17.** Same build. **B 5.** No filename in the repo, so the brand lives only in CI logs. **O 7.** Freeze plus gating are still distinctive. Kept as K1b's fallback for teams that ban generated files.

### K6: AI-session impact block (70)
- **R 24.** AI-assisted edits happen daily for many developers (hypothesis; the README pitches this use). **W 19.** Fits agent hooks. **F 14.** Without a stored map, each session needs a 15–25 s upload (E§3). **B 6.** Visible only inside the assistant's transcript. **O 7.** Merged into K1b as the `impact` command.

### K19: maintainer triage label (70)
- **R 21.** Daily for popular OSS repos. **W 18.** Labels are quiet and filterable. **F 17.** Computable from a stored map. **B 6.** A label name carries little brand. **O 8.** It answers a 2026-specific maintainer pain (hypothesis: the flood of AI-generated PRs). Folded into K1b's reach line.

### K15: architecture rules (69)
- **R 23 / W 17 / F 15 / B 7 / O 7.** Rule authoring is friction, and import-linter and dependency-cruiser already exist (`CL`). Its useful core, freeze, is folded into K1b.

### K2: PR comment bot, hosted per PR (68)
- **R 24.** Automatic. **W 20.** In the PR. **F 13.** A hosted upload on every push, the LLM for business impact (down for my whole trial, E§3) and a 2-slot service (`/health`). **B 8.** **O 3.** Most-proposed (crowd 9).

### K7: branded context pack (65)
- **R 20 / W 18 / F 17 / B 6 / O 4.** Useful and feasible: `selections.jsonl` already holds Narrow/Optimal/Wider packs per file (E§2). But Repomix owns the category, and the brand line in a pasted prompt is read mostly by the model. Kept as a secondary `context` command.

### Lower-ranked candidates (one-line reasons)
- **K16 AGENTS.md section (64):** cheap, but humans rarely see it. Brand is weak.
- **K5 post-merge catch-up (63):** a good moment, but it needs an upload per pull or a stored map (K1b provides `git log -p UNVIBECODE.md`).
- **K12 weekly bot PR (63):** Dependabot cadence. Weekly reviews of an unchanged map are noise when structure didn't change.
- **K9 VS Code extension (62):** best ease of access, but it has no trigger of its own, needs the 15–25 s hosted wait, and is the most-proposed channel.
- **K3 pre-commit check (58):** a commit-time upload at 11–26 s wall is too slow for a hook (E§3); already public (#312).
- **K14, K17, K18, K8 (53–56):** real moments, but monthly or rarer.
- **K20 affected tests (56):** demoted by evidence. The transitive closure saturates on Flask (74 of 74 dependents), and fixture shadowing would route test edges wrongly.
- **K4 since-last diff (53):** already public (#291). Built on LLM outputs reported as non-deterministic (#408, #516).
- **K10, K13, K11 (43–49):** gimmicky, noisy, or built on non-deterministic LLM scores.
