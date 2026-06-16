import random

from playwright.sync_api import Locator, expect

from src.models.product import Product
from src.pages.base_page import BasePage


class ProductsPage(BasePage):
    product_cards_selector = ".features_items .product-image-wrapper"

    def open_products(self) -> None:
        self.open("/products")
        expect(self.page.locator(".features_items")).to_be_visible()

    def select_random_products(self, count: int = 2) -> list[Product]:
        cards = self._available_cards()
        if len(cards) < count:
            raise AssertionError(f"Expected at least {count} products, found {len(cards)}")

        selected_indexes = random.sample(range(len(cards)), count)
        selected_products: list[Product] = []
        for index in selected_indexes:
            card = cards[index]
            selected_products.append(self._product_from_card(card))
            self._add_to_cart(card)
        return selected_products

    def _available_cards(self) -> list[Locator]:
        cards = self.page.locator(self.product_cards_selector)
        return [
            cards.nth(index)
            for index in range(cards.count())
            if cards.nth(index).locator('a.add-to-cart[data-product-id]').count() > 0
        ]

    @staticmethod
    def _product_from_card(card: Locator) -> Product:
        info = card.locator(".productinfo")
        name = info.locator("p").inner_text().strip()
        price = info.locator("h2").inner_text().strip()
        return Product(name=name, price=price, quantity=1)

    def _add_to_cart(self, card: Locator) -> None:
        card.locator('a.add-to-cart[data-product-id]').first.click()
        self.page.get_by_role("button", name="Continue Shopping").click()
