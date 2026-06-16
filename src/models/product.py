from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    name: str
    price: str
    quantity: int = 1
    total_price: str | None = None
