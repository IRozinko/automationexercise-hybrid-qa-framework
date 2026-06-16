from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self, path: str = "/") -> None:
        self.page.goto(path, wait_until="domcontentloaded")

    def accept_cookie_banner_if_present(self) -> None:
        consent = self.page.get_by_role("button", name="Consent")
        if consent.count() > 0:
            consent.first.click()
