from dataclasses import dataclass
from order_types import OrderTypes


@dataclass
class OrderData():
    order_type: OrderTypes
    price: int
    quantity: int
    trader_id: int

    