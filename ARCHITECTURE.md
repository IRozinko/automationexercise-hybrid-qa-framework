# Architecture

## Layered Design

The framework separates orchestration from implementation details:

- `tests/`: scenario intent and business-level assertions.
- `src/flows/`: readable workflow composition across multiple pages.
- `src/pages/`: Page Object Model classes and UI locators.
- `src/api/`: backend account setup and teardown.
- `src/models/`: typed data structures for users and products.
- `src/data/`: factories that create unique test payloads.
- `src/utils/`: reporting helpers and address parsing.
- `conftest.py`: Pytest fixtures and failure artifact hooks.

## API Layer

`AccountClient` owns Automation Exercise account endpoint calls. Tests do not
build raw API requests directly; they receive a registered user fixture and rely
on teardown to delete it. This keeps cleanup centralized and easier to harden.

## Page Objects

Page objects expose user actions and page-specific assertions:

- `LoginPage`: opens login and authenticates an existing user.
- `ProductsPage`: opens catalog, finds addable product cards, captures product
  name/price, and adds selected products.
- `CartPage`: reads cart rows, verifies selected products, and proceeds to
  checkout.
- `CheckoutPage`: reads and parses the delivery address block.

Selectors prefer semantic text, data attributes, and stable page structure from
the target site.

## Fixtures

Fixtures handle lifecycle and cross-cutting concerns:

- `generated_user`: creates unique user data.
- `registered_user`: creates and deletes the backend account.
- `browser`, `context`, `page`: manage Playwright lifecycle.
- `pytest_runtest_makereport`: exposes test outcome to teardown hooks.

The context fixture starts Playwright tracing for every test. Failure teardown
stores the trace, and the page fixture captures screenshot and HTML source.

## Data Models And Factories

`User` maps framework field names to the account API payload. `Product` stores
the catalog/cart attributes used for assertions. `UserFactory` creates unique,
reviewable data without relying on external files or shared accounts.

## Reporting And Artifacts

Allure is used for human-readable execution evidence. Steps are added around
major business actions, and structured JSON attachments preserve selected
products and address comparison data. Failure artifacts are available in both
Allure and the local `artifacts/` directory.

## Extending The Framework

A QA team can extend this structure by adding:

- new API clients under `src/api`;
- additional page objects under `src/pages`;
- reusable workflows under `src/flows`;
- factories for other domain data under `src/data`;
- markers and workflow jobs for smoke, regression, and nightly execution;
- cross-browser or environment matrices in GitHub Actions.
