from pydantic import BaseModel, ConfigDict


class RestaurantBase(BaseModel):
    name: str
    address: str


class RestaurantCreate(RestaurantBase):
    owner_id: int


class RestaurantRead(RestaurantBase):
    id: int
    is_active: bool
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
