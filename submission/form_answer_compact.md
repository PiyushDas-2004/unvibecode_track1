**1. Recommended approach**

`unvibe`: a command developers type after they, or their AI assistant, change code. It says which UnvibeCode business workflows the change touched, offline in about 0.1 s, from a committed `UNVIBECODE.md` that stores the Business Workflow Map and Connected Code Map. Each PR shows the same line as a quiet "UnvibeCode" check.

**2. Supporting points**

- **Deliberate and named, unlike MCP.** On django-payments PR #501 (uncommitted), `unvibe` printed "touches provider-backed payment checkout and callback handling (StripeProviderV3.get_form, create_session)" in 76 ms. Reviewers see the same line in the PR checks list.
- **Built on what worked.** In my 0.4.0 trial the LLM stage failed 10 of 10 runs (credits exhausted). The code map succeeded in 1.5–3.7 s with identical re-runs. So the LLM refreshes the index weekly, a failed refresh keeps the old index, and each answer is a local lookup. All 8 django-payments commits after the 18 Oct map were classified correctly.
- **Memorable.** Workflow names are vocabulary only UnvibeCode produces, and the file sits next to README.md.

**3. Implementation plan**

Build `unvibe`, `unvibecode map` and a one-check Actions template on the existing outputs (my prototype has 38 tests). Run 4 weeks on 20–30 Python/Go repos against a control. Success is at least 3 manual `unvibe` runs per developer per week, counted separately from CI.

Prototype and evidence: https://github.com/PiyushDas-2004/unvibecode/tree/claude/unvibecode-track2-adoption-yqgmiv
