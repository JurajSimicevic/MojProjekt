from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.core.phases import OrderStatus

class OrderCreate(BaseModel):
    """Schema za kreiranje nove narudžbe."""
    restaurant_id: int
    item_ids: list[int]

class OrderRead(BaseModel):
    """Schema za prikaz detalja narudžbe."""
    id: int
    customer_id: int
    restaurant_id: int
    courier_id: int | None
    total_price: float
    status: OrderStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
