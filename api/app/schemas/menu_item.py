from pydantic import BaseModel, ConfigDict


class MenuItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    is_available: bool = True


class MenuItemCreate(MenuItemBase):
    restaurant_id: int


class MenuItemRead(MenuItemBase):
    id: int
    restaurant_id: int

    model_config = ConfigDict(from_attributes=True)
