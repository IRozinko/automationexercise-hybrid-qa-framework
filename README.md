# Automation Exercise Hybrid QA Framework

Draft framework for validating a hybrid API/UI checkout scenario on
https://automationexercise.com.

The project uses Python, Pytest, Playwright, requests, and Allure. The first
revision defines the architecture, fixtures, data model, API client skeleton,
page object skeletons, and CI-ready repository layout.

## Current Scope

- Generate a unique user dataset.
- Create and delete accounts through the backend API.
- Exercise login, product selection, cart verification, and checkout address
  validation through the UI.
- Keep browser lifecycle, test data, and cleanup behind Pytest fixtures.

## Planned Execution

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
pytest
```
