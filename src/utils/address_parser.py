from src.models.user import User


def expected_delivery_address(user: User) -> dict[str, str]:
    return {
        "name": f"{user.title}. {user.first_name} {user.last_name}",
        "company": user.company,
        "address1": user.address1,
        "address2": user.address2,
        "city_state_zip": f"{user.city} {user.state} {user.zipcode}",
        "country": user.country,
        "mobile_number": user.mobile_number,
    }
