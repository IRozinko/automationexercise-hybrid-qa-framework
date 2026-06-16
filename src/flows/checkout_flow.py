from playwright.sync_api import Page


class CheckoutFlow:
    def __init__(self, page: Page) -> None:
        self.page = page
