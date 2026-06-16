# Test Execution Results

Execution date: 2026-06-16

Environment:

- Python: `python3` with project virtual environment `.venv` locally and
  Python 3.11.15 in GitHub Actions
- Browser: Playwright Chromium installed successfully
- Target: `https://automationexercise.com`

## Commands Run

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/playwright install chromium
python3 -m compileall conftest.py src tests
.venv/bin/python -m pytest --collect-only -q
.venv/bin/python -m pytest -q
```

GitHub Actions run from commit `4035750`:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install --with-deps chromium
pytest
```

## Results

| Check | Result | Notes |
| --- | --- | --- |
| Dependency installation | Passed | Installed packages from `requirements.txt`. |
| Playwright Chromium installation | Passed | Chromium and headless shell downloaded. |
| Python compilation | Passed | `conftest.py`, `src`, and `tests` compiled successfully. |
| Pytest collection | Passed | `1 test collected`. |
| Local full E2E execution | Blocked by target site | Local sandbox traffic returned Imunify360 bot-protection. |
| GitHub Actions full E2E execution | Passed | `1 passed in 5.35s`. |
| Allure artifact upload | Passed | `allure-results` artifact uploaded successfully. |

## Local E2E Blocker

The local sandbox run reached the API setup phase, but the public target site
blocked automation traffic from this environment. A browser-like request to the
public products API returned:

```text
Access denied by Imunify360 bot-protection. IPs used for automation should be whitelisted
```

The framework is ready to run from an allowed local network, whitelisted CI
runner, or test environment without this bot-protection block.

## CI Result

The GitHub Actions runner completed the full hybrid API/UI test successfully:

```text
tests/test_checkout_delivery_address.py . [100%]
1 passed in 5.35s
```

The successful run did not produce failure artifacts, so the workflow uploads
`artifacts/` only on failed runs and ignores a missing directory.

## Assumptions

- Account API response codes follow the Automation Exercise contract:
  `201` for creation and `200` for deletion.
- The checkout delivery address format remains the current seven-line block:
  name, company, address lines, city/state/zip, country, mobile.
- Random product selection is acceptable because the test captures the exact
  selected product data before cart assertions.
