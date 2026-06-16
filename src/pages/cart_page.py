from playwright.sync_api import expect

from src.models.product import Product
from src.pages.base_page import BasePage


class CartPage(BasePage):
    def open_cart(self) -> None:
        self.open("/view_cart")
        expect(self.page.locator("#cart_info_table")).to_be_visible()

    def products(self) -> list[Product]:
        rows = self.page.locator("#cart_info_table tbody tr")
        products: list[Product] = []
        for index in range(rows.count()):
            row = rows.nth(index)
            name = row.locator(".cart_description h4 a").inner_text().strip()
            price = row.locator(".cart_price p").inner_text().strip()
            quantity = int(row.locator(".cart_quantity button").inner_text().strip())
            total_price = row.locator(".cart_total p").inner_text().strip()
            products.append(
                Product(
                    name=name,
                    price=price,
                    quantity=quantity,
                    total_price=total_price,
                )
            )
        return products

    def assert_products_match(self, expected_products: list[Product]) -> None:
        actual_by_name = {product.name: product for product in self.products()}
        missing = [product.name for product in expected_products if product.name not in actual_by_name]
        assert not missing, f"Products missing from cart: {missing}. Actual: {actual_by_name}"

        for expected in expected_products:
            actual = actual_by_name[expected.name]
            assert actual.price == expected.price, (
                f"Cart price mismatch for {expected.name}: "
                f"expected {expected.price}, got {actual.price}"
            )
            assert actual.quantity == expected.quantity, (
                f"Cart quantity mismatch for {expected.name}: "
                f"expected {expected.quantity}, got {actual.quantity}"
            )
            if actual.total_price:
                assert actual.total_price == expected.price, (
                    f"Cart total mismatch for {expected.name}: "
                    f"expected {expected.price}, got {actual.total_price}"
                )

    def proceed_to_checkout(self) -> None:
        self.page.locator(".check_out").click()
        expect(self.page.locator("#address_delivery")).to_be_visible()
