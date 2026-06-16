from src.pages.base_page import BasePage
from src.utils.address_parser import parse_delivery_address


class CheckoutPage(BasePage):
    def delivery_address(self) -> dict[str, str]:
        items = self.page.locator("#address_delivery li")
        lines = [
            items.nth(index).inner_text().strip()
            for index in range(items.count())
            if items.nth(index).inner_text().strip()
        ]
        return parse_delivery_address(lines)
