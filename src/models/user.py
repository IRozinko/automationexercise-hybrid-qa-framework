from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class User:
    name: str
    email: str
    password: str
    title: str
    birth_day: str
    birth_month: str
    birth_year: str
    first_name: str
    last_name: str
    company: str
    address1: str
    address2: str
    country: str
    state: str
    city: str
    zipcode: str
    mobile_number: str

    def as_api_payload(self) -> dict[str, str]:
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "title": self.title,
            "birth_date": self.birth_day,
            "birth_month": self.birth_month,
            "birth_year": self.birth_year,
            "firstname": self.first_name,
            "lastname": self.last_name,
            "company": self.company,
            "address1": self.address1,
            "address2": self.address2,
            "country": self.country,
            "zipcode": self.zipcode,
            "state": self.state,
            "city": self.city,
            "mobile_number": self.mobile_number,
        }

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
