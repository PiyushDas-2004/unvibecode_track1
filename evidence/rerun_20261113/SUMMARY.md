# Re-run of the UnvibeCode trial (2026-11-13 16:42 UTC)

## Environment
- OS: Windows-11-10.0.26300-SP0
- Python: Python 3.12.7
- unvibecode: 0.4.0 (install 4.2 s)
- health: {'status': 'ok', 'service': 'unvibecode-engine', 'busy': False, 'presentation_version': 1, 'analysis_slots': 2}

## UnvibeCode runs (`python -m unvibecode review --repository <repo> --output <dir> --no-open-browser`)

| Repository | Commit | Wall | CLI summary | Code-map lane | Business lane | Reason | Business Workflow Map produced |
|---|---|---|---|---|---|---|---|
| flask | `49943b5a` | 18.7 s | UNVIBECODE REVIEW PARTIAL · 12s | COMPLETED (2.034 s) | FAILED | The hosted analysis service has exhausted its API credits | no |
| node-express-realworld-example-app | `30b68e1e` | 8.1 s | UNVIBECODE REVIEW PARTIAL · 5s | COMPLETED (0.916 s) | FAILED | The hosted analysis service has exhausted its API credits | no |
| spring-petclinic | `500158f7` | 5.9 s | UNVIBECODE REVIEW PARTIAL · 2s | COMPLETED (1.175 s) | SKIPPED_UNSUPPORTED_REPOSITORY | No usable supported application connections; detected: css, html, java No hosted workflow analysis was started | no |
| microservices-demo | `c7cb6d5b` | 21.1 s | UNVIBECODE REVIEW PARTIAL · 13s | COMPLETED (2.035 s) | FAILED | The hosted analysis service has exhausted its API credits | no |
| django-payments | `5607e9e8` | 8.3 s | UNVIBECODE REVIEW PARTIAL · 6s | COMPLETED (1.078 s) | FAILED | The hosted analysis service has exhausted its API credits | no |

## Prototype
- Tests: passed (Ran 38 tests)
- django-payments workflows used: UnvibeCode published sample (business analysis unavailable in this run)
- `unvibe` on PR #501 as an uncommitted change: 797 ms

```
UnvibeCode business reach: this change touches 1 business workflow(s)
  provider-backed payment checkout and callback handling [Payment workflows]: changed StripeProviderV3, StripeProviderV3.create_session, StripeProviderV3.get_form in payments/stripe/providers.py
Code reach: 2 changed file(s); 1 other file(s) import them directly.
  payments/stripe/providers.py: 1 direct importer(s)
      changed symbol StripeProviderV3 is used by payments/stripe/__init__.py
  1 changed file(s) have no recorded importers.
Import lines changed in payments/stripe/test_stripev3.py: structure may have changed; run `unvibecode-mapfile check`.
```

Commits after the 18 Oct map: see django-payments_after_18_oct.txt
