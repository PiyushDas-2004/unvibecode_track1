**1. Approach:** `unvibe`, a command developers type after they (or their AI) change code. It names the UnvibeCode business workflows touched, offline in about 0.1 s, from a committed `UNVIBECODE.md`. Each PR shows the same line as an "UnvibeCode" check.

**2. Why:** It is deliberate and named, unlike MCP. On django-payments PR #501 it found the Stripe checkout workflow in 76 ms. My 0.4.0 trial's LLM stage failed 10 of 10 runs, so the LLM only refreshes the index weekly and every answer is a local lookup. All 8 later commits were classified correctly.

**3. Plan:** Build `unvibe` and `unvibecode map` (prototype has 38 tests). Run 4 weeks on 20–30 repos. Success: at least 3 manual runs per developer per week.

Repo: https://github.com/PiyushDas-2004/unvibecode/tree/claude/unvibecode-track2-adoption-yqgmiv
