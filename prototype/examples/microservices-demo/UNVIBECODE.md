# UnvibeCode Map: microservices-demo

> The [UnvibeCode](https://github.com/FinanceFlash/unvibecode) Business Workflow Map and Connected Code Map for this repository, kept as text so git can diff it and every clone carries it.
> What does my change touch? `unvibe` · Refresh: `unvibecode-mapfile build` · Check a pull request: `unvibecode-mapfile check`
> Written by unvibecode-mapfile (community prototype, not an official UnvibeCode product). Do not edit by hand.

<!-- unvibecode-map:v1 source_files=74 connected_files=22 connections=17 unresolved_relative_imports=1 -->

## Business workflows

Not available yet: UnvibeCode's business analysis has not produced a workflow map for this repository. The sections below still work.

## Most-imported files

Change these with care: many files connect to them directly.

| File | Direct importers |
|---|---:|
| `src/paymentservice/logger.js` | 2 |
| `src/productcatalogservice/catalog_loader.go` | 2 |
| `src/shippingservice/quote.go` | 2 |
| `src/shippingservice/tracker.go` | 2 |
| `src/checkoutservice/money/money.go` | 1 |
| `src/frontend/middleware.go` | 1 |
| `src/frontend/money/money.go` | 1 |
| `src/frontend/packaging_info.go` | 1 |
| `src/frontend/rpc.go` | 1 |
| `src/frontend/validator/validator.go` | 1 |
| `src/paymentservice/charge.js` | 1 |
| `src/paymentservice/server.js` | 1 |
| `src/shippingservice/main.go` | 1 |

## Area connections

| From | To | Connections |
|---|---|---:|
| (none) | every recorded connection stays inside one area | 0 |

## Check these connections

None found.

## Coverage

- Source files analysed: 74
- Files with at least one connection: 22 (29%)
- Relative imports UnvibeCode could not resolve: 1

## Connections

One line per connected file pair, with the symbols used. Line numbers are left out on purpose, so this section only changes when structure changes.

### `src/checkoutservice/money/money_test.go`
- → `src/checkoutservice/money/money.go` · AreEquals, AreSameCurrency, IsNegative, IsPositive, IsValid, IsZero, Must, Negate, Sum

### `src/frontend/handlers.go`
- → `src/frontend/packaging_info.go` · httpGetPackagingInfo, isPackagingServiceConfigured
- → `src/frontend/rpc.go` · convertCurrency, emptyCart, getAd, getCart, getCurrencies, getProduct, getProducts, getRecommendations, getShippingQuote, insertCart

### `src/frontend/main.go`
- → `src/frontend/middleware.go` · ensureSessionID

### `src/frontend/money/money_test.go`
- → `src/frontend/money/money.go` · AreEquals, AreSameCurrency, IsNegative, IsPositive, IsValid, IsZero, Must, Negate, Sum

### `src/frontend/validator/validator_test.go`
- → `src/frontend/validator/validator.go` · Validate

### `src/paymentservice/index.js`
- → `src/paymentservice/logger.js`
- → `src/paymentservice/server.js`

### `src/paymentservice/server.js`
- → `src/paymentservice/charge.js`
- → `src/paymentservice/logger.js`

### `src/productcatalogservice/product_catalog.go`
- → `src/productcatalogservice/catalog_loader.go` · loadCatalog

### `src/productcatalogservice/server.go`
- → `src/productcatalogservice/catalog_loader.go` · loadCatalog

### `src/shippingservice/main.go`
- → `src/shippingservice/quote.go` · CreateQuoteFromCount
- → `src/shippingservice/tracker.go` · CreateTrackingId

### `src/shippingservice/shippingservice_test.go`
- → `src/shippingservice/main.go` · GetQuote, ShipOrder
- → `src/shippingservice/quote.go` · CreateQuoteFromCount, CreateQuoteFromFloat, String
- → `src/shippingservice/tracker.go` · CreateTrackingId, getRandomLetterCode, getRandomNumber
