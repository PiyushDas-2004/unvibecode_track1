# Ideas other Claude-assisted competitors will almost certainly submit

Crowdedness: 10 = expect a large share of entries to propose it; 1 = rare. Where the idea is already public as an upstream issue, the issue number is given. That is hard evidence of crowding, not a guess.

| # | Idea | Crowdedness | Public evidence | Why it is crowded / what a vague version misses |
|---|---|---|---|---|
| C01 | VS Code extension with a sidebar code map | 9 | #472 mentions IDE ecosystems | The first channel anyone names. A vague version ignores that output needs the hosted service (15–25 s) and has no daily trigger. |
| C02 | GitHub Action that comments on every PR | 9 | #476, #683 | Generic. Ignores PR-comment noise, the 2 analysis slots and LLM credit cost per PR. |
| C03 | Pre-commit hook / `check --staged` | 8 | **#312** (with `unvibe` alias) | Already public. Uploading on every commit is too slow (15–25 s) and costly. |
| C04 | "What changed since last review" diff | 8 | **#291**, **#289** | Already public. Built on LLM outputs that are non-deterministic (#408). |
| C05 | PR business-impact (diff → workflows → risks) | 7 | **#683** | Already public. Needs the LLM stage, which was down. |
| C06 | README badge ("Unvibed", score, workflows count) | 8 | **#457** | Vanity metric; brand only, no use. |
| C07 | Workflow/health scorecard with a number that moves | 6 | **#457** | Gamifies a non-deterministic LLM output. |
| C08 | Slack/Teams bot or daily digest | 7 | – | Notification fatigue; requires a server and an install. |
| C09 | Weekly email digest | 6 | – | Easy to ignore; email is not where code work happens. |
| C10 | Web playground: paste a GitHub URL | 8 | upstream PUBLIC_PREVIEW asks people to email requests | Gets first-time users, not repeat users. |
| C11 | Chrome extension on github.com | 6 | – | Store review, permissions; a second product to maintain. |
| C12 | Docker image / Homebrew / pipx / npx wrapper | 7 | #476, #472 | Fixes access, not return visits. |
| C13 | CLI `--watch` mode | 5 | – | Re-uploads continuously; no clear trigger. |
| C14 | Streaks / gamification / XP | 5 | #291 ("like a fitness tracker") | Developer-hostile when it isn't backed by real value. |
| C15 | MCP server + "visible" branding inside the assistant | 7 | #506, #629, challenge brief | The brief explicitly says MCP alone is not enough. |
| C16 | JSON/Markdown output formats + `--format` flag | 7 | #472 | Necessary plumbing, not a reason to return. |
| C17 | Onboarding wizard / interactive TUI | 6 | #338, #394 | Fixes first run only. |
| C18 | Jira/Linear ticket integration ("where to change for this ticket") | 4 | – | Needs the LLM; integration-heavy. |
| C19 | Shareable hosted report links | 6 | – | Job IDs are bearer tokens; privacy. |
| C20 | Telemetry dashboard of D1/D7 metrics | 5 | – | Measurement is not an adoption mechanism. |
| C21 | Use the 18 workflow packs as checklists | 4 | **#457** | Already public. |
| C22 | Git post-merge "catch-up" briefing | 3 | – | Less common, but still a hook on a run-to-run diff. |
| C23 | Generic "AI context packer" like Repomix (`unvibe ctx file | pbcopy`) | 5 | – | Repomix already owns this; brand recall unclear. |
| C24 | Stack-trace explainer (`unvibe trace`) | 3 | – | Rare, but LLM assistants already do this well. |
| C25 | Architecture docs auto-generated into the repo | 5 | – | Plausible; usually proposed vaguely ("generate docs") with no freshness mechanism. |

## How I use this list

1. Any candidate whose core is C01–C06 gets a crowdedness of 7+ in scoring. It has to win on a **mechanism** none of the public proposals has.
2. The public proposals share a weakness my trial exposed: they run the hosted analysis, often the LLM stage, **on every trigger**. That conflicts with the observed failure mode (credits exhausted), the 2-slot capacity and the upload-permission problem. A design that **uploads rarely and answers locally** is different in mechanism, even if it touches the same surface (PRs, commits).
3. "Steal-from-yourself" test: if three competent people given the brief would land on the same core idea, push it further.
