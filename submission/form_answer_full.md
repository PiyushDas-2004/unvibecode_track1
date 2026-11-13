**1. Recommended approach**

Make `unvibe` the command a developer types right after they, or their AI assistant, change code. It answers in UnvibeCode's own terms which business workflows the change touched, in about 0.1 s, offline. It reads a committed `UNVIBECODE.md` that stores the Business Workflow Map and Connected Code Map. Every pull request shows the same one-line answer as a quiet "UnvibeCode" check.

**2. Supporting points**

- **A daily trigger the developer chooses, by name.** AI-written code is now the everyday "unfamiliar code" moment UnvibeCode was built for. I applied django-payments PR #501 as an uncommitted change and typed `unvibe`. In 76 ms it printed: "touches 1 business workflow: provider-backed payment checkout and callback handling (StripeProviderV3.get_form, create_session)". Unlike an invisible MCP call, the developer types the name and comes back on purpose. Reviewers see the same line in the PR checks list, so they learn the name too.

- **Built on what worked in my trial, and cheap to run daily.** On version 0.4.0 the hosted business stage failed on 10 of 10 runs ("exhausted its API credits"). The Connected Code Map succeeded every time in 1.5–3.7 s, with byte-identical re-runs. So the LLM refreshes the workflow index only weekly, and a failed refresh keeps the previous index. Every per-change answer is a local lookup with no upload. I built the map at django-payments' 18 October commit and tested all 8 commits merged afterwards. Every one was classified correctly (5 touched a workflow), after fixing two matching bugs that the hand-check found.

- **Memorable because the answer is UnvibeCode's, not a generic graph.** Workflow names like "PayPal checkout and post-payment reconciliation" are the vocabulary only UnvibeCode produces. People remember a product by the words it gives them. `UNVIBECODE.md` sits next to README.md, so teammates and AI agents can read it with nothing installed. It also flags engine mistakes openly, such as 43 Flask files whose `import flask` resolves to a test fixture.

**3. Implementation plan**

Build first (days): `unvibe` (also `git unvibe`), and `unvibecode map`, which writes `UNVIBECODE.md` from the existing context ZIP and the Business Workflow Map. Add a GitHub Actions template that posts one neutral check. My prototype does all of this in stdlib Python with 38 passing tests. Test for 4 weeks on 20–30 active Python/Go repos against a control group that has only `unvibecode review`. The primary metric is manual `unvibe` runs per developer per week, with CI runs counted separately. Success: a median of at least 3 a week by weeks 3–4 and D7 return of at least 40%. Stop if it stays under 1 a week.

Prototype, evidence and real outputs: https://github.com/PiyushDas-2004/unvibecode/tree/claude/unvibecode-track2-adoption-yqgmiv
