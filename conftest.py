from pathlib import Path
import re

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from src.api.account_client import AccountClient
from src.config.settings import settings
from src.data.user_factory import UserFactory
from src.models.user import User


def _artifact_name(nodeid: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", nodeid).strip("_")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="session")
def account_client() -> AccountClient:
    return AccountClient(base_url=settings.base_url)


@pytest.fixture()
def generated_user() -> User:
    return UserFactory.build()


@pytest.fixture()
def registered_user(account_client: AccountClient, generated_user: User) -> User:
    with allure.step(f"Create test account via API: {generated_user.email}"):
        account_client.create_account(generated_user)
    try:
        yield generated_user
    finally:
        with allure.step(f"Delete test account via API: {generated_user.email}"):
            account_client.delete_account(generated_user.email, generated_user.password)


@pytest.fixture(scope="session")
def browser() -> Browser:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=settings.headless,
            slow_mo=settings.slow_mo_ms,
        )
        yield browser
        browser.close()


@pytest.fixture()
def context(browser: Browser, request: pytest.FixtureRequest) -> BrowserContext:
    context = browser.new_context(base_url=settings.base_url)
    context.set_default_timeout(settings.default_timeout_ms)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    trace_dir = Path(settings.artifacts_dir) / "traces"
    trace_dir.mkdir(parents=True, exist_ok=True)
    trace_path = trace_dir / f"{_artifact_name(request.node.nodeid)}.zip"
    if failed:
        context.tracing.stop(path=str(trace_path))
        allure.attach.file(
            str(trace_path),
            name="Playwright trace",
            extension="zip",
        )
    else:
        context.tracing.stop()
    context.close()


@pytest.fixture()
def page(context: BrowserContext, request: pytest.FixtureRequest) -> Page:
    page = context.new_page()
    yield page
    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    if failed:
        artifact_dir = Path(settings.artifacts_dir) / "failures"
        artifact_dir.mkdir(parents=True, exist_ok=True)
        name = _artifact_name(request.node.nodeid)

        screenshot_path = artifact_dir / f"{name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        allure.attach.file(
            str(screenshot_path),
            name="Failure screenshot",
            attachment_type=allure.attachment_type.PNG,
        )

        source = page.content()
        source_path = artifact_dir / f"{name}.html"
        source_path.write_text(source, encoding="utf-8")
        allure.attach(
            source,
            name="Failure page source",
            attachment_type=allure.attachment_type.HTML,
        )
