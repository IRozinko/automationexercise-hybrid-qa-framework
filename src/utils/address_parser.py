from src.models.user import User


def expected_delivery_address(user: User) -> dict[str, str]:
    return {
        "name": _normalize_name(f"{user.title}. {user.first_name} {user.last_name}"),
        "company": user.company,
        "address1": user.address1,
        "address2": user.address2,
        "city_state_zip": f"{user.city} {user.state} {user.zipcode}",
        "country": user.country,
        "mobile_number": user.mobile_number,
    }


def parse_delivery_address(lines: list[str]) -> dict[str, str]:
    values = [line.strip() for line in lines if line.strip()]
    if values and values[0].lower() == "your delivery address":
        values = values[1:]

    if len(values) < 6:
        raise AssertionError(f"Unexpected delivery address format: {lines}")

    return {
        "name": _normalize_name(values[0]),
        "company": values[1],
        "address1": values[2],
        "address2": values[3],
        "city_state_zip": values[4],
        "country": values[5],
        "mobile_number": values[6] if len(values) > 6 else "",
    }


def _normalize_name(value: str) -> str:
    return " ".join(value.replace(".", "").split())
