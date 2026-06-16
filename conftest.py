import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from src.api.account_client import AccountClient
from src.config.settings import settings
from src.data.user_factory import UserFactory
from src.models.user import User


@pytest.fixture(scope="session")
def account_client() -> AccountClient:
    return AccountClient(base_url=settings.base_url)


@pytest.fixture()
def generated_user() -> User:
    return UserFactory.build()


@pytest.fixture()
def registered_user(account_client: AccountClient, generated_user: User) -> User:
    account_client.create_account(generated_user)
    try:
        yield generated_user
    finally:
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
def context(browser: Browser) -> BrowserContext:
    context = browser.new_context(base_url=settings.base_url)
    context.set_default_timeout(settings.default_timeout_ms)
    yield context
    context.close()


@pytest.fixture()
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    yield page
