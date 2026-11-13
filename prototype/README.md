# unvibecode-mapfile + `unvibe` (community prototype)

**Type `unvibe` and see which business workflows your change touches, in about 0.1 s, offline. The same line appears on every pull request as a quiet "UnvibeCode" check.**

It works by keeping UnvibeCode's output in the repository as `UNVIBECODE.md`:
- **Business Workflow index:** workflow names → files and symbols, from UnvibeCode's Business Workflow Map.
- **Connected Code Map:** file → file connections with symbols.

Both are line-free, so git can diff them and later commits don't invalidate them.

This is a community prototype for the UnvibeCode Engineering Challenge 2026 (Cohort 3, Track 2). It is **not an official UnvibeCode product**. It reads UnvibeCode's documented outputs: the repository-context ZIP and the Business Workflow Map page. It contains no UnvibeCode engine code.

## Why this shape (from the brief and from my trial)

| The brief asks | How this answers it |
|---|---|
| Not MCP alone, because users "benefit … without remembering its name or deliberately returning to it" | The developer **types the name** (`unvibe` or `git unvibe`) at a moment they already have: after an AI assistant or they themselves changed code, before committing. |
| "memorable as a product" | The answer is in UnvibeCode's own vocabulary, the **business workflow** ("provider-backed payment checkout and callback handling"). An import-graph tool can't say that. |
| "easy to access" | One `build`, then `unvibe` works offline with no upload. Teammates and AI agents read `UNVIBECODE.md` with nothing installed. |
| "useful during daily development … return tomorrow or next week" | Every change gets an answer, and every PR shows the same line in its checks list. The index lives in git, so its history accumulates. |

The trial also set three rules for the design:
1. **Keep the LLM out of the per-change loop.** The hosted business stage failed with "exhausted its API credits" on 10/10 of my runs, and upstream issues #408 and #516 report non-deterministic workflow output. The workflow index is refreshed on purpose (weekly or per release). If a refresh can't produce workflows, the previous index is **kept**.
2. **Line-free keys.** A 19-line Flask edit moved 97 chunk IDs but 0 connections. A real refactor moved exactly +3/−2.
3. **Show errors.** A *Check these connections* section flags suspicious edges, such as 43 Flask files whose `import flask` points to a 3-line test fixture.

## Run it in under 5 minutes (no network)

Requires Python 3.11+ and git. No dependencies.

```bash
git clone https://github.com/PiyushDas-2004/unvibecode.git
cd unvibecode/prototype
python -m unittest discover -s tests            # 38 tests on real UnvibeCode output

# Build the django-payments map: real code-map bundle + UnvibeCode's published Business Workflow Map
python -m unvibecode_mapfile build --bundle fixtures/django-payments_5607e9e.zip \
    --workflows fixtures/django-payments_5607e9e_business-workflows.html --map /tmp/UNVIBECODE.md
sed -n 1,25p /tmp/UNVIBECODE.md
```

To see `unvibe` on a real change, use django-payments PR #501, merged after the map date:

```bash
git clone -q https://github.com/jazzband/django-payments.git /tmp/dp
git -C /tmp/dp checkout -q 5607e9e
git -C /tmp/dp diff 529d6a5~1 529d6a5 -- payments/ | git -C /tmp/dp apply      # PR #501, uncommitted
python -m unvibecode_mapfile impact --repository /tmp/dp --map /tmp/UNVIBECODE.md   # = `unvibe` inside /tmp/dp
```

Expected output (recorded in [`examples/django-payments/unvibe_uncommitted_log.txt`](examples/django-payments/unvibe_uncommitted_log.txt)):

```
UnvibeCode business reach: this change touches 1 business workflow(s)
  provider-backed payment checkout and callback handling [Payment workflows]: changed StripeProviderV3, StripeProviderV3.create_session, StripeProviderV3.get_form in payments/stripe/providers.py
Code reach: 2 changed file(s); 1 other file(s) import them directly.
  ...
```

(After `pip install ./` the same thing is just `unvibe`, typed inside the repository.)

## Use it on your own repository (live; uploads to the hosted UnvibeCode service)

```bash
python -m pip install --upgrade unvibecode
python -m pip install ./                 # installs: unvibecode-mapfile, unvibe, git-unvibe
cd /path/to/your/repo
unvibecode-mapfile build                 # one hosted run; picks up the Business Workflow Map if UnvibeCode produced one
git add UNVIBECODE.md && git commit -m "Add UnvibeCode map"
# ... you or your AI assistant edit code ...
unvibe                                   # or: git unvibe   (local, about 0.1 s, nothing uploaded)
```

Results go to a temporary folder that is **deleted after use**, so nothing lands in `git status` except `UNVIBECODE.md`.

## Commands

| Command | What it does | Network |
|---|---|---|
| `unvibe` / `git unvibe` (= `impact`) `[--base REF] [--head REF] [--markdown] [--oneline]` | Business workflows touched (exact enclosing `Class.method` for Python, from the before/after files), then code reach (direct importers, changed symbols they use, hubs), then whether an import line changed | none |
| `build [--bundle ZIP] [--workflows HTML]` | Writes `UNVIBECODE.md`. Without new workflows it keeps the previous index. Prints "Unchanged" when nothing changed. | 1 hosted run, or none with `--bundle` |
| `check [--since REF] [--strict]` | Freeze check: connections added/removed versus the committed file. Skips the upload when no import line changed in a source file. Warn-only by default. | 0 or 1 hosted run |
| `diff OLD NEW` | Structural delta between two map files or git revisions | none |

**Surfaces:**
- [`ci-example/.github/workflows/unvibecode-map.yml`](ci-example/.github/workflows/unvibecode-map.yml) publishes one neutral check run named **UnvibeCode**, with the `--oneline` text as its title, in the PR's checks list. It posts no comment.
- [`agent-example/.claude/commands/unvibe.md`](agent-example/.claude/commands/unvibe.md) is a `/unvibe` slash command for Claude Code that the developer types deliberately. It shows the `unvibe` output and asks the assistant to use UnvibeCode's workflow names.

*Neither file was executed on GitHub or inside Claude Code for this submission. Every command in them was run locally.*

## Evidence from real repositories

See [`examples/SOURCES.md`](examples/SOURCES.md) and [`/evidence/business_reach_verification.md`](../evidence/business_reach_verification.md).

- **django-payments, "next week" test.** I built the map at `5607e9e` (18 Oct), then ran `unvibe --oneline` on all 8 commits merged after it. 5 touched a business workflow (PR #501 → "provider-backed payment checkout and callback handling") and 3 touched none (config, changelog, tests). I checked all 8 by hand, and all 8 are correct. That came after fixing two matcher bugs that the hand check found:
  - a hunk header blamed the function above an edited `def` line;
  - a change inside `BasePayment.save` wasn't credited to `BasePayment`.
- **Flask.** A day-1 map with 18 flagged suspicious connections. The freeze check on refactor `c2705ff` gives exactly +3/−2. A 30-line map diff covers a 36-file refactor.
- **TypeScript and Java.** The file states the gaps plainly. realworld-example has 2 connections and 49 unresolved relative imports, flagged as a "Sparse map".

## How we would measure repeat usage

**Events.** Opt-in and local only: set `UNVIBECODE_MAPFILE_USAGE_LOG=/path/usage.jsonl`. Each command appends `{event, ts, trigger: ci|manual, entry: unvibe|impact, workflows_touched, changed_files, uploaded}`. Nothing is sent anywhere. Upstream would offer the same events as an explicit opt-in to anonymous counters.

**Proxy with no telemetry.** In public repos the artifact is public. GitHub code search for `UNVIBECODE.md` with the `unvibecode-map:v1` marker counts adopting repos, and `git log UNVIBECODE.md` shows refreshes.

**Metrics.**
- **Primary:** weekly *manual* `unvibe` runs per active developer. This is the brief's "deliberately returning"; CI runs are counted separately so automation can't inflate it.
- D1/D7/D30 return rate per developer (ran `unvibe` again within 1/7/30 days of the first run).
- Share of PRs whose UnvibeCode check named at least one business workflow.
- Repo retention: `UNVIBECODE.md` still present and refreshed at day 30.

**Experiment.**
- *Cohort:* 20–30 active Python or Go repositories (where my trial showed the map is reliable), each with at least 2 contributors.
- *Arms:* the treatment gets `UNVIBECODE.md`, `unvibe` and the CI check. The control gets `unvibecode review` only.
- *Duration:* 4 weeks.
- *Success:* median of at least 3 manual `unvibe` runs per active developer per week in weeks 3–4, D7 developer return of at least 40%, and at least 50% of treatment repos still refreshing the file at day 30. Control: under 1 manual run per week.
- *Kill:* under 1 manual run per developer per week by week 3, or more than 1 in 5 workflow hits judged wrong by the developers who received them.

## Limitations

- **Workflow quality is UnvibeCode's.** I couldn't generate a Business Workflow Map myself (credits exhausted on 10/10 runs), so the demo uses UnvibeCode's published django-payments map. My verification covers the *matching* of changes to that map, not how good its workflows are.
- **Refreshing needs the hosted service.** That means an upload approval for private repos, from CI or a lead, and only at refresh time. 0.3.x built the code map locally, so a local mode is possible upstream.
- **Language coverage.** Python matching is exact (enclosing scope from indentation). Other languages fall back to git hunk headers and definition lines. TypeScript and Java code maps were thin or empty in the trial.
- **What counts as "touched".** Formatting-only edits still count as touching a workflow (django-payments `f0e1f2c`).
- **Suspicious-edge heuristics** catch the errors I found and will miss others.
- **Example files were not run in place.** The CI and agent files are examples, not run on GitHub Actions or in Claude Code.

## Ideal upstream integration

- `unvibecode map`, `unvibecode map --check` and `unvibe` as subcommands of the official CLI.
- The Business Workflow Map also emitted as JSON with symbol references, instead of parsing HTML.
- The bundle README renamed from "ShipReady" to UnvibeCode.
- If the business model allows, the deterministic lane run locally again.

License: MIT (this prototype). UnvibeCode is licensed by its owners; see their [licensing clarification](https://github.com/FinanceFlash/unvibecode/blob/main/docs/LICENSE_CLARIFICATION.md).
