import allure
import pytest

from src.flows.checkout_flow import CheckoutFlow
from src.utils.allure_utils import attach_json
from src.utils.address_parser import expected_delivery_address


@allure.epic("Automation Exercise")
@allure.feature("Hybrid checkout")
@allure.story("Delivery address validation")
@allure.title("API-created user sees matching delivery address during checkout")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("layer", "e2e")
@pytest.mark.e2e
@pytest.mark.ui
@pytest.mark.api
@pytest.mark.smoke
def test_checkout_delivery_address_matches_registered_user(page, registered_user):
    """Hybrid API setup plus UI checkout scenario."""
    checkout = CheckoutFlow(page)

    checkout.login(registered_user)
    selected_products = checkout.add_random_products_to_cart(count=2)
    attach_json("Selected products", [product.__dict__ for product in selected_products])

    checkout.open_cart_and_verify(selected_products)
    actual_address = checkout.proceed_to_checkout_and_read_delivery_address()

    expected_address = expected_delivery_address(registered_user)
    attach_json("Expected delivery address", expected_address)
    attach_json("Actual delivery address", actual_address)

    assert actual_address == expected_address, (
        "Delivery address mismatch. "
        f"Expected: {expected_address}. Actual: {actual_address}"
    )
