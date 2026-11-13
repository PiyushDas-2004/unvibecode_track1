# UnvibeCode Map: django-payments

> The [UnvibeCode](https://github.com/FinanceFlash/unvibecode) Business Workflow Map and Connected Code Map for this repository, kept as text so git can diff it and every clone carries it.
> What does my change touch? `unvibe` · Refresh: `unvibecode-mapfile build` · Check a pull request: `unvibecode-mapfile check`
> Written by unvibecode-mapfile (community prototype, not an official UnvibeCode product). Do not edit by hand.

<!-- unvibecode-map:v1 source_files=62 connected_files=45 connections=82 unresolved_relative_imports=0 -->

## Business workflows

7 workflows from the UnvibeCode Business Workflow Map. Refreshed on purpose (weekly or per release), not on every change. Line numbers are left out so later commits do not invalidate it.

### Workflow · provider-backed payment checkout and callback handling
Area: Payment workflows

- `payments/__init__.py` · PaymentError.__init__, PaymentStatus, get_payment_model
- `payments/core.py` · BasicProvider.__init__, BasicProvider.cancel, BasicProvider.capture, BasicProvider.get_action, BasicProvider.get_form, BasicProvider.get_hidden_fields, BasicProvider.get_return_url, BasicProvider.get_token_from_request, BasicProvider.process_data, BasicProvider.refund, BasicProvider.release, _default_provider_factory, get_base_url
- `payments/dummy/__init__.py` · DummyProvider, DummyProvider.get_form, DummyProvider.process_data
- `payments/mercadopago/__init__.py` · MercadoPagoProvider, MercadoPagoProvider.create_preference, MercadoPagoProvider.get_form, MercadoPagoProvider.process_callback, MercadoPagoProvider.process_notification
- `payments/stripe/providers.py` · StripeProviderV3, StripeProviderV3.create_session, StripeProviderV3.get_form, StripeProviderV3.process_data

### Workflow · card payment authorization and capture via Authorize.Net
Area: Payment workflows

- `payments/authorizenet/__init__.py` · AuthorizeNetProvider, AuthorizeNetProvider.__init__, AuthorizeNetProvider.get_form, AuthorizeNetProvider.get_payment_response
- `payments/authorizenet/forms.py` · PaymentForm, PaymentForm.clean
- `payments/authorizenet/test_authorizenet.py` · test_provider_redirects_to_success_on_payment_success
- `payments/models.py` · BasePayment

### Workflow · card payment authorization and settlement
Area: Payment workflows

- `payments/braintree/__init__.py` · BraintreeProvider, BraintreeProvider.__init__, BraintreeProvider.get_form
- `payments/braintree/forms.py` · BraintreePaymentForm, BraintreePaymentForm.clean, BraintreePaymentForm.save
- `payments/braintree/test_braintree.py` · test_provider_redirects_to_success_on_payment_success, test_provider_shows_validation_error_message
- `payments/models.py` · BasePayment

### Workflow · Provider-specific payment request composition and callback verification
Area: Payment workflows

- `payments/coinbase/__init__.py` · CoinbaseProvider, CoinbaseProvider.get_checkout_code, CoinbaseProvider.get_custom_token, CoinbaseProvider.process_data
- `payments/coinbase/test_coinbase.py` · test_incorrect_custom_token_process_data, test_incorrect_data_process_data, test_process_data
- `payments/dotpay/__init__.py` · DotpayProvider, DotpayProvider.process_data
- `payments/dotpay/forms.py` · ProcessPaymentForm, ProcessPaymentForm.clean, ProcessPaymentForm.save
- `payments/dotpay/test_dotpay.py` · test_get_hidden_fields, test_incorrect_process_data, test_process_data_payment_accepted, test_process_data_payment_rejected

### Workflow · PayPal checkout and post-payment reconciliation
Area: Payment workflows

- `payments/paypal/__init__.py` · PaypalProvider, PaypalProvider.capture, PaypalProvider.get_access_token, PaypalProvider.get_form, PaypalProvider.process_data, PaypalProvider.refund, authorize, authorize.wrapper
- `payments/paypal/test_paypal.py` · Payment, test_provider_captures_payment, test_provider_raises_redirect_needed_on_success, test_provider_refunds_payment_fully, test_provider_renews_access_token, test_provider_request_without_payerid_redirects_on_failure

### Workflow · gateway-specific checkout callback handling
Area: Payment workflows

- `payments/cybersource/__init__.py` · CyberSourceProvider, CyberSourceProvider.__init__, CyberSourceProvider._change_status_to_confirmed, CyberSourceProvider._set_proper_payment_status_from_reason_code, CyberSourceProvider.charge, CyberSourceProvider.process_data
- `payments/models.py` · BasePayment
- `payments/sagepay/__init__.py` · SagepayProvider, SagepayProvider.get_hidden_fields, SagepayProvider.process_data
- `payments/sofort/test_sofort.py` · test_provider_raises_redirect_needed_on_success, test_provider_redirects_on_success

### Workflow · Process provider callback to update a payment record
Area: Callback workflows

- `payments/coinbase/__init__.py` · CoinbaseProvider.process_data
- `payments/dotpay/__init__.py` · DotpayProvider.process_data
- `payments/test_urls.py` · ProcessDataLockingTestCase, ProcessDataLockingTestCase.test_process_data_locks_the_payment_row, StaticCallbackTestCase.test_invalid_provider_variant_returns_json_400, StaticCallbackTestCase.test_payment_not_found_returns_json_404
- `payments/urls.py` · process_data, static_callback

## Most-imported files

Change these with care: many files connect to them directly.

| File | Direct importers |
|---|---:|
| `payments/__init__.py` | 33 |
| `payments/core.py` | 16 |
| `payments/forms.py` | 9 |
| `payments/models.py` | 5 |
| `payments/utils.py` | 3 |
| `docs/conf.py` | 2 |
| `payments/dotpay/forms.py` | 2 |
| `payments/fields.py` | 2 |
| `payments/authorizenet/forms.py` | 1 |
| `payments/braintree/forms.py` | 1 |
| `payments/cybersource/forms.py` | 1 |
| `payments/dummy/forms.py` | 1 |
| `payments/mercadopago/__init__.py` | 1 |
| `payments/paypal/forms.py` | 1 |
| `payments/signals.py` | 1 |

## Area connections

| From | To | Connections |
|---|---|---:|
| `testapp` | `payments` | 4 |
| `payments` | `docs` | 2 |
| `docs` | `payments` | 1 |

## Check these connections

None found.

## Coverage

- Source files analysed: 62
- Files with at least one connection: 45 (72%)
- Relative imports UnvibeCode could not resolve: 0

## Connections

One line per connected file pair, with the symbols used. Line numbers are left out on purpose, so this section only changes when structure changes.

### `docs/conf.py`
- → `payments/__init__.py`

### `payments/__init__.py`
- → `docs/conf.py`

### `payments/authorizenet/__init__.py`
- → `payments/__init__.py` · PaymentStatus, RedirectNeeded
- → `payments/authorizenet/forms.py` · PaymentForm
- → `payments/core.py` · BasicProvider

### `payments/authorizenet/forms.py`
- → `payments/__init__.py` · PaymentStatus
- → `payments/forms.py` · CreditCardPaymentForm

### `payments/authorizenet/test_authorizenet.py`
- → `payments/__init__.py` · PaymentStatus, RedirectNeeded

### `payments/braintree/__init__.py`
- → `payments/__init__.py` · PaymentStatus, RedirectNeeded
- → `payments/braintree/forms.py` · BraintreePaymentForm
- → `payments/core.py` · BasicProvider

### `payments/braintree/forms.py`
- → `payments/__init__.py` · PaymentStatus
- → `payments/forms.py` · CreditCardPaymentFormWithName

### `payments/braintree/test_braintree.py`
- → `payments/__init__.py` · PaymentStatus, RedirectNeeded

### `payments/coinbase/__init__.py`
- → `payments/__init__.py` · PaymentStatus
- → `payments/core.py` · BasicProvider

### `payments/coinbase/test_coinbase.py`
- → `payments/__init__.py` · PaymentStatus, PurchasedItem

### `payments/core.py`
- → `docs/conf.py`
- → `payments/forms.py`
- → `payments/models.py`

### `payments/cybersource/__init__.py`
- → `payments/__init__.py` · ExternalPostNeeded, FraudStatus, PaymentError, PaymentStatus, RedirectNeeded
- → `payments/core.py` · BasicProvider, get_credit_card_issuer
- → `payments/cybersource/forms.py` · PaymentForm
- → `payments/forms.py` · PaymentForm

### `payments/cybersource/forms.py`
- → `payments/__init__.py` · PaymentError
- → `payments/forms.py` · CreditCardPaymentFormWithName

### `payments/cybersource/test_cybersource.py`
- → `payments/__init__.py` · PaymentStatus, PurchasedItem, RedirectNeeded
- → `payments/core.py`

### `payments/dotpay/__init__.py`
- → `payments/core.py` · BasicProvider
- → `payments/dotpay/forms.py` · ProcessPaymentForm

### `payments/dotpay/forms.py`
- → `payments/__init__.py` · PaymentStatus

### `payments/dotpay/test_dotpay.py`
- → `payments/__init__.py` · PaymentStatus
- → `payments/dotpay/forms.py` · COMPLETED, REJECTED

### `payments/dummy/__init__.py`
- → `payments/__init__.py` · PaymentError, PaymentStatus, RedirectNeeded
- → `payments/core.py` · BasicProvider
- → `payments/dummy/forms.py` · DummyForm

### `payments/dummy/forms.py`
- → `payments/__init__.py` · FraudStatus, PaymentStatus
- → `payments/forms.py` · PaymentForm

### `payments/dummy/test_dummy.py`
- → `payments/__init__.py` · FraudStatus, PaymentError, PaymentStatus, RedirectNeeded

### `payments/fields.py`
- → `payments/core.py` · CARD_TYPES, get_credit_card_issuer
- → `payments/utils.py` · get_month_choices, get_year_choices
- → `payments/widgets.py` · CreditCardExpiryWidget, CreditCardNumberWidget

### `payments/forms.py`
- → `payments/fields.py` · CreditCardExpiryField, CreditCardNameField, CreditCardNumberField, CreditCardVerificationField

### `payments/mercadopago/__init__.py`
- → `payments/__init__.py` · PaymentError, PaymentStatus, RedirectNeeded
- → `payments/core.py` · BasicProvider
- → `payments/models.py`

### `payments/mercadopago/test_mercadopago.py`
- → `payments/__init__.py` · PaymentError, PaymentStatus, PurchasedItem, RedirectNeeded
- → `payments/mercadopago/__init__.py` · MercadoPagoProvider

### `payments/models.py`
- → `payments/core.py`
- → `payments/signals.py`

### `payments/paypal/__init__.py`
- → `payments/__init__.py` · PaymentError, PaymentStatus, RedirectNeeded
- → `payments/core.py` · BasicProvider, get_credit_card_issuer
- → `payments/paypal/forms.py` · PaymentForm
- → `payments/utils.py`

### `payments/paypal/forms.py`
- → `payments/__init__.py` · PaymentStatus
- → `payments/core.py` · get_credit_card_issuer
- → `payments/forms.py` · CreditCardPaymentFormWithName

### `payments/paypal/test_paypal.py`
- → `payments/__init__.py` · PaymentError, PaymentStatus, PurchasedItem, RedirectNeeded
- → `payments/utils.py`

### `payments/sagepay/__init__.py`
- → `payments/__init__.py` · PaymentStatus
- → `payments/core.py` · BasicProvider
- → `payments/models.py`

### `payments/sagepay/test_sagepay.py`
- → `payments/__init__.py` · PaymentStatus

### `payments/sofort/__init__.py`
- → `payments/__init__.py` · PaymentError, PaymentStatus, RedirectNeeded
- → `payments/core.py` · BasicProvider

### `payments/sofort/test_sofort.py`
- → `payments/__init__.py` · PaymentStatus, RedirectNeeded

### `payments/stripe/__init__.py`
- → `payments/stripe/providers.py` · StripeProviderV3

### `payments/stripe/providers.py`
- → `payments/__init__.py` · PaymentError, PaymentStatus, RedirectNeeded
- → `payments/core.py` · BasicProvider
- → `payments/forms.py` · PaymentForm

### `payments/stripe/test_stripev3.py`
- → `payments/__init__.py` · PaymentError, PaymentStatus, PurchasedItem, RedirectNeeded

### `payments/test_core.py`
- → `payments/__init__.py`
- → `payments/forms.py` · CreditCardPaymentFormWithName, PaymentForm
- → `payments/models.py` · BasePayment

### `payments/test_fields.py`
- → `payments/fields.py` · CreditCardNumberField

### `payments/test_urls.py`
- → `payments/__init__.py` · PaymentError

### `payments/urls.py`
- → `payments/core.py`

### `testapp/testapp/testmain/forms.py`
- → `payments/__init__.py` · get_payment_model

### `testapp/testapp/testmain/models.py`
- → `payments/__init__.py` · PurchasedItem
- → `payments/models.py` · BasePayment

### `testapp/testapp/testmain/views.py`
- → `payments/__init__.py` · RedirectNeeded, get_payment_model
- → `testapp/testapp/testmain/forms.py` · TestPaymentForm
