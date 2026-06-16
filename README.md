# Automation Exercise Hybrid QA Framework

Python-based hybrid API/UI automation framework for the checkout delivery
address scenario on https://automationexercise.com.

The framework is designed for a senior QA review: API setup and teardown are
separated from browser actions, UI behavior is modeled through Page Objects, test
data is generated through a factory, and reporting captures enough context to
debug failures without rerunning immediately.

## Why This Stack

- Playwright: resilient locators, built-in tracing, modern browser automation,
  and deterministic waiting without fixed sleeps.
- Pytest: fixture composition, clear test metadata, concise assertions, and
  simple CI execution.
- Allure: readable test narratives, structured attachments, and failure
  artifacts for review.
- requests: small, explicit API client layer for account setup and cleanup.

## Prerequisites

- Python 3.10+
- Java Runtime Environment and Allure commandline for local HTML report
  generation
- Network access to `automationexercise.com`
- Chromium browser installed through Playwright

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

## Running Tests

Headless mode is the default:

```bash
pytest
```

Headed mode:

```bash
HEADLESS=false pytest
```

Useful environment variables:

- `BASE_URL`: target host, default `https://automationexercise.com`
- `HEADLESS`: `true` or `false`, default `true`
- `SLOW_MO_MS`: optional Playwright slow motion in milliseconds
- `DEFAULT_TIMEOUT_MS`: locator/action timeout, default `15000`
- `ARTIFACTS_DIR`: local failure artifacts directory, default `artifacts`

## Allure Report

Test runs write raw Allure results to `allure-results/`.

```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

On failure the framework attaches a full-page screenshot, the current page
source, and a Playwright trace archive to the Allure result.

## Project Structure

```text
.
├── conftest.py
├── requirements.txt
├── pytest.ini
├── src
│   ├── api
│   ├── config
│   ├── data
│   ├── flows
│   ├── models
│   ├── pages
│   └── utils
├── tests
├── .github/workflows/tests.yml
├── ARCHITECTURE.md
├── TEST_STRATEGY.md
└── TEST_EXECUTION_RESULTS.md
```

## Covered Scenario

The E2E test creates a unique user through the backend API, logs in through the
UI, selects two random available products, verifies cart name/price/quantity and
line totals, proceeds to checkout, parses the delivery address block, and
compares it with the generated registration data. The account is deleted through
the API during fixture teardown even when UI steps fail.

## Test Data Strategy

`UserFactory` creates a unique email and address payload per test run. Product
selection is intentionally random, but only from product cards that expose a
valid add-to-cart action. Selected product attributes are captured before adding
items to the cart and attached to Allure for traceability.

## Failure Artifacts

When a test fails, `conftest.py` captures:

- full-page screenshot;
- current HTML source;
- Playwright trace zip.

The local files are stored under `artifacts/`, while Allure receives the same
debug payload as attachments.

## CI

`.github/workflows/tests.yml` installs Python dependencies, installs Playwright
Chromium, runs Pytest, and uploads Allure results plus failure artifacts.

## Known Limitations And Assumptions

- The target site may block automation traffic with Imunify360 unless the runner
  IP is allowed. See `TEST_EXECUTION_RESULTS.md`.
- Product inventory and UI copy belong to the public demo site and may change.
- Checkout payment submission is intentionally out of scope; the scenario stops
  at delivery address validation.
- No retries are enabled. Failures should remain visible until a concrete
  flakiness pattern justifies `pytest-rerunfailures`.
