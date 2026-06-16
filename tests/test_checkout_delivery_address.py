import pytest

from src.flows.checkout_flow import CheckoutFlow
from src.utils.address_parser import expected_delivery_address


@pytest.mark.e2e
@pytest.mark.ui
@pytest.mark.api
@pytest.mark.smoke
def test_checkout_delivery_address_matches_registered_user(page, registered_user):
    """Hybrid API setup plus UI checkout scenario."""
    checkout = CheckoutFlow(page)

    checkout.login(registered_user)
    selected_products = checkout.add_random_products_to_cart(count=2)
    checkout.open_cart_and_verify(selected_products)
    actual_address = checkout.proceed_to_checkout_and_read_delivery_address()

    expected_address = expected_delivery_address(registered_user)
    assert actual_address == expected_address, (
        "Delivery address mismatch. "
        f"Expected: {expected_address}. Actual: {actual_address}"
    )
