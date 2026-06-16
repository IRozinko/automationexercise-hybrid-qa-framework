import pytest


@pytest.mark.e2e
@pytest.mark.ui
@pytest.mark.api
@pytest.mark.smoke
def test_checkout_delivery_address_matches_registered_user(page, registered_user):
    """Hybrid API setup plus UI checkout scenario."""
    raise NotImplementedError
