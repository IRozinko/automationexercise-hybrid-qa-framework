from src.pages.base_page import BasePage


class LoginPage(BasePage):
    def open_login(self) -> None:
        self.open("/login")

    def login(self, email: str, password: str) -> None:
        self.page.locator('[data-qa="login-email"]').fill(email)
        self.page.locator('[data-qa="login-password"]').fill(password)
        self.page.locator('[data-qa="login-button"]').click()
        self.page.get_by_text("Logged in as").wait_for()
