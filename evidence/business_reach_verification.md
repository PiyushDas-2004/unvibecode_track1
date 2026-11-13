# Business reach: hand verification on real django-payments history (13 Nov 2026)

**Map:** `prototype/examples/django-payments/UNVIBECODE.md`.
- Code map: a live UnvibeCode 0.4.0 run on jazzband/django-payments @ `5607e9e88762df9831980832c194f49b227dbe93`, the last commit on or before 18 Oct 2026.
- Workflows: UnvibeCode's own published Business Workflow Map sample for django-payments dated 2026-10-18 (FinanceFlash/unvibecode `docs/gitdocs/django-payments/2026-10-18/report-support/business-workflows.html`). I used it because the hosted LLM stage returned "exhausted its API credits" on all 10 of my runs (latest 15:48 UTC). 6 of its implementation references were checked against `5607e9e`, and all match line for line: `core.py:146 def capture`, `core.py:70 def get_action`, `stripe/providers.py:98 def get_form`, `mercadopago/__init__.py:150 def process_callback`, `__init__.py:30 class PaymentStatus`, `dummy/__init__.py:16 class DummyProvider`.

**Test:** every commit merged after the map date (`5607e9e..47449a1`, 8 commits), checked by hand against `git diff -U0` with the Python diff driver.

| Commit | Subject | UnvibeCode said | Hand check |
|---|---|---|---|
| ff5082a | Fix dict being used as a set | 3 workflows via `BasePayment` (models.py) | Correct: the change is inside `BasePayment.save` (models.py:103). Those 3 workflows reference `BasePayment`. *v1 of the matcher said "file shared"; fixed with Python scopes.* |
| 3f3001d | pre-commit autoupdate | none | Correct: config only |
| 49c4bb3 | Fix ruff ICN001 datetime alias | gateway-specific checkout callback handling, via `CyberSourceProvider.process_data` | Correct: `dt.date(...)` inside `process_data` (line 487). Import line flagged too. |
| f0e1f2c | pre-commit.ci auto fixes | same workflow, `process_data` | Correct but formatting-only (one call reflowed) |
| 529d6a5 | stripe: support stripe>=15 (#501) | provider-backed payment checkout: `StripeProviderV3.get_form`, `create_session` | Correct: `get_form` (line 101) and `create_session` (line 142) changed |
| 2105d02 | Update changelog | none | Correct |
| d1eea51 | Add more type hints to stripe logic | provider-backed checkout: `StripeProviderV3.create_session` | Correct. *v1 also blamed `get_form`, because git's hunk header names the function above an edited `def` line. Fixed and covered by a regression test.* |
| 47449a1 | Add tests for stripe conversion | none (test file not referenced by any workflow) | Correct per the map |

**Result:** after the two fixes, 8 of 8 commits are classified correctly against the map. 5 touched at least one business workflow. 1 of those 5 was a formatting-only change.

This tests the *matching*, not the quality of UnvibeCode's workflow extraction, which I could not run myself.
