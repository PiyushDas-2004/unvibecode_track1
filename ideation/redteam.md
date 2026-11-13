# Red team

Three adversarial personas attacked each top-5 candidate.
- **Founder:** a skeptical Alphashots.AI founder. "Will developers actually come back? Can a small team build and run it?"
- **Rival:** a contestant arguing their idea is better.
- **Jaded engineer:** a senior engineer who hates tools that add noise to PRs and terminals.

Verdicts: **survives**, **revise**, **merge**, **eliminate**.

---

## Round 1 (after pass 1)

### K1: committed map file (80)
- **Founder:** "Flask's internal imports changed in 6% of commits, about 0.1 a week (your own churn data). If the file rarely changes, why would anyone run the tool weekly?" **Hit.** A structural delta alone is too rare on mature repos.
- **Rival (PR-bot camp):** "My Action comments on every PR automatically. Yours waits for someone to regenerate a file." **Partial hit.** K1 also runs in CI, but only on structural PRs.
- **Jaded engineer:** "A generated file in my repo, plus a red CI check whenever it's stale? I'll delete both." **Hit**, if the check blocks by default.
- **Verdict: revise.** Add a per-PR reach line computed locally from the committed file, so every PR gets value. Make the check warn-only by default. Mark the file `linguist-generated` so GitHub collapses its diff. Report only deltas (freeze). This became **K1b** in pass 2.

### K6: AI-session impact block (70)
- **Founder:** "Where does the map come from at the end of each assistant session? Another 15–25 s upload every time?" **Hit.**
- **Rival:** "Isn't this MCP with extra steps? The brief says invisible assistant integrations aren't enough." **Partial hit.** The block is printed visibly, but it lives inside the assistant's UI.
- **Jaded engineer:** "Every edit prints a block in my agent transcript. Noise." **Hit.**
- **Verdict: merge into K1b.** `impact` reads the committed map with no upload. Developers run it when they choose, or wire it into an agent hook.

### K15: architecture rules from the map (69)
- **Founder:** "Who writes the rules? No team will write import rules for a tool they tried once." **Hit.**
- **Rival:** "import-linter and dependency-cruiser already do this, without uploading code." **Hit.**
- **Jaded engineer:** "One more config file to maintain." **Hit.**
- **Verdict: merge into K1b as freeze semantics.** The committed map *is* the rule set: the current state is allowed, and anything new gets reported. No rules to write (ArchUnit FreezingArchRule pattern, verified).

### K2: PR comment bot with a hosted run per PR (68)
- **Founder:** "Every PR push uploads the repo and wants the LLM for impact. The LLM was out of credits for your whole trial, and the service has 2 slots." **Hit, backed by evidence.**
- **Rival:** "It's the most automatic trigger there is." **True.** That's why it's popular (#476, #683).
- **Jaded engineer:** "One more bot comment on every PR, even when nothing structural changed. Muted within a week." **Hit.**
- **Verdict: eliminate as stand-alone.** Re-scored in pass 3 as K22, the same surface rebuilt on the K1b engine, which ranks second.

### K7: branded context pack for AI chats (65)
- **Founder:** "Repomix already owns 'pack my repo for an LLM'. What's our edge?" Connected selections are a real edge, but users have no reason to remember the name. **Hit.**
- **Rival:** "The brand line in a pasted prompt is read by the model, not by people." **Hit.**
- **Jaded engineer:** "Fine, I'd use it occasionally." Neutral.
- **Verdict: keep as a secondary command (`context`), not as the approach.**

---

## Round 2 (after pass 3): attacking K1b, the committed, self-checking map file (84)

### Founder
1. *"Will they come back?"* Return triggers come from events that already happen. (a) **Every PR** gets a reach line in the CI job summary. (b) **Structural PRs** get a freeze delta asking the author to refresh the file, the way a stale lockfile does. On netbox that is about 9 commits a week (measured). (c) **The file itself** is opened by new teammates and AI agents. The tool runs because work happens, not because someone has to remember it. **Survives.**
2. *"Can a small team build it?"* v0 is a thin layer over the existing context ZIP. My prototype is about 550 lines of stdlib Python with tests, built in a day on real bundles. **Survives.**
3. *"Does it cost us money?"* No LLM calls in the loop. Uploads happen only when an import line changes (6–37% of commits measured). Server time 1.5–3.7 s per refresh. **Survives.**
4. *"What about private repos?"* Only CI uploads, and only on structural PRs. Teammates reading the file or running `impact` upload nothing. That's much less exposure than per-developer runs, but it still needs one approval. **Partial: stated honestly as a limitation.**

### Rival
1. *"PR impact is already public (#683)."* #683 asks for a diff → workflows → risks analysis that needs the LLM and a full re-run. K1b reports structure deterministically from a committed baseline, with no LLM and no per-PR upload. Same surface, different mechanism. **Survives**, but I take −1 originality (pass 2).
2. *"A committed file is just ARCHITECTURE.md."* An ARCHITECTURE.md is written by hand, goes stale and nothing checks it. K1b is regenerated, checked in CI, diffed by freeze semantics, and queryable by a CLI. That's what separates a lockfile from a hand-written list of packages. **Survives.**
3. *"My VS Code extension is where developers actually live."* Then it can read `UNVIBECODE.md`. The file works as the data layer for any later surface. **Survives.**

### Jaded engineer
1. *"Generated noise in my PR diffs."* The file changes only when cross-file structure changes. In my trial that was 0 changes across two multi-commit ranges, and 5 lines on a big refactor. `.gitattributes: UNVIBECODE.md linguist-generated=true` collapses it by default. **Survives.**
2. *"CI going red because a map is stale."* Warn-only by default (exit 0, job summary only). `--strict` is opt-in. **Survives.**
3. *"It'll be wrong and I'll stop trusting it."* It *is* wrong sometimes (Flask fixture shadowing, `helpers.py → tests/conftest.py`). K1b flags suspicious edges in their own section, so the error is visible and reportable instead of buried in a graph. **Revised (S113 added).**
4. *"I don't want any generated file in git."* `--no-commit` mode (S114) keeps the baseline as a CI artifact. **Revised.**

**Round-2 verdict: K1b survives with three additions (S113 suspicious-edge section, S114 no-commit mode, S115 day-1 onboarding render). The core loop is unchanged.**


---

## Round 3 (after pass 4): attacking A+B, a committed UnvibeCode map with a Business Workflow index, opened deliberately with `unvibe` and echoed in a quiet PR check title (88)

### Founder
1. *"You depend on our LLM stage, which your own logs show was down."* Only the **refresh** of the workflow index needs it (weekly or per release). Per-change answers are lookups. When a refresh can't produce workflows, `build` **keeps the previous index** (tested: `KeepsWorkflowsWhenBusinessAnalysisIsDown`). An outage makes the index older; it doesn't break the daily loop. Cost: one LLM run per repo per week instead of one per PR. **Survives.**
2. *"Is 'workflow touched' right?"* I checked 8 real django-payments commits merged after the 18 Oct map by hand. After fixing two matcher bugs I found during that check, all 8 are correct (evidence/business_reach_verification.md). One true positive was formatting-only. **Survives, with that caveat stated.**
3. *"Will people type `unvibe`?"* Unproven, and it's the main hypothesis. The experiment counts manual runs separately from CI runs, and the kill criteria use them. **Accepted as the main risk.**

### Rival
1. *"#683 already proposed business impact for PRs."* #683 re-runs the LLM per PR. A+B never does, and adds the deliberate command, the committed index, and verified matching. **Survives.**
2. *"Your import-graph version (v1) was enough."* v1 failed the brief's "remember its name / deliberately return" test, and anyone's import graph tool could produce its output. Workflow names are UnvibeCode's own output. **A+B is strictly better.**

### Jaded engineer
1. *"A bot in my PRs."* No comment. One neutral check run whose title is one line. **Survives.**
2. *"LLM workflow names churn and spam diffs."* The index changes only on a deliberate refresh, in its own PR. **Survives.**
3. *"`unvibe` on my laptop uploads my code?"* No. `unvibe` reads `UNVIBECODE.md` and `git diff` only; it took 76–100 ms in the examples. **Survives.**

**Round-3 verdict: A+B survives. Residual risk: whether developers type the command daily. The experiment is designed around that.**
