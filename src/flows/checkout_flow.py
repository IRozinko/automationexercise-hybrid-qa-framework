from playwright.sync_api import Page

from src.models.product import Product
from src.models.user import User
from src.pages.cart_page import CartPage
from src.pages.checkout_page import CheckoutPage
from src.pages.login_page import LoginPage
from src.pages.products_page import ProductsPage


class CheckoutFlow:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.login_page = LoginPage(page)
        self.products_page = ProductsPage(page)
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)

    def login(self, user: User) -> None:
        self.login_page.open_login()
        self.login_page.login(user.email, user.password)

    def add_random_products_to_cart(self, count: int = 2) -> list[Product]:
        self.products_page.open_products()
        return self.products_page.select_random_products(count=count)

    def open_cart_and_verify(self, expected_products: list[Product]) -> None:
        self.cart_page.open_cart()
        self.cart_page.assert_products_match(expected_products)

    def proceed_to_checkout_and_read_delivery_address(self) -> dict[str, str]:
        self.cart_page.proceed_to_checkout()
        return self.checkout_page.delivery_address()
