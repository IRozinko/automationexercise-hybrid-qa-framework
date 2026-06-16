# Test Strategy

## Scope

The current automated scope covers one critical hybrid journey:

1. Create a unique user through `POST /api/createAccount`.
2. Log in through the browser UI.
3. Add two random available products to the cart.
4. Verify product data in the cart.
5. Validate checkout delivery address against registration data.
6. Delete the generated user through `DELETE /api/deleteAccount`.

Out of scope: payment completion, email delivery, visual comparison, cross-device
layout coverage, and exhaustive catalog validation.

## Hybrid API/UI Strategy

API setup keeps the browser scenario focused on user-facing behavior instead of
spending time on registration screens. UI validation then covers the flows that
matter to a customer: login, catalog interaction, cart review, and checkout
address rendering. API teardown removes the generated account independently of
the UI outcome.

## Risk-Based Coverage

High-value assertions are concentrated around data continuity:

- the user can authenticate with API-created credentials;
- selected product names and prices survive catalog-to-cart transitions;
- cart quantity and total values are correct for single-quantity items;
- checkout delivery address matches the registered user.

## Test Data Management

`UserFactory` generates a unique email and address payload for every run. This
avoids shared test accounts and reduces data coupling between runs. Product
selection is random but constrained to cards with available add-to-cart actions.

## Cleanup Strategy

The `registered_user` fixture wraps test execution in `try/finally` and calls
the account deletion endpoint after the test body, even when browser steps fail.
Deletion tolerates an already-missing user response so cleanup remains idempotent.

## Flakiness Mitigation

- No fixed sleeps.
- Playwright locators and assertions are used for browser synchronization.
- Browser context lifecycle is isolated per test.
- Selected product data is captured before interaction and reused for assertions.
- Failure artifacts include screenshot, page source, and trace.

## Reporting Strategy

Allure labels describe the test layer and business feature. Allure steps narrate
API setup, login, product selection, cart verification, checkout parsing, and API
teardown. JSON attachments include selected products, expected address, and
actual parsed address.

## Future Improvements

- Add API contract tests for account endpoints and products list.
- Add deterministic product selection mode through a seed for repeat debugging.
- Add separate smoke and nightly suites.
- Add browser matrix coverage after the Chromium path is stable.
- Add static checks such as Ruff or mypy.
- Add a whitelisted CI runner or proxy strategy if the public demo site blocks
  hosted automation traffic.
