from dataclasses import dataclass


@dataclass
class Item:
    sku: str
    qty: int
    price: float
