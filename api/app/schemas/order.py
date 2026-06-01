from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.phases import OrderStatus


class OrderCreate(BaseModel):
    restaurant_id: int
    item_ids: list[int]


class OrderItemRead(BaseModel):
    id: int
    menu_item_id: int
    item_name: str
    price_at_purchase: float

    model_config = ConfigDict(from_attributes=True)


class OrderRead(BaseModel):
    id: int
    customer_id: int
    restaurant_id: int
    courier_id: int | None
    total_price: float
    status: OrderStatus
    created_at: datetime
    items: list[OrderItemRead] = []

    model_config = ConfigDict(from_attributes=True)
