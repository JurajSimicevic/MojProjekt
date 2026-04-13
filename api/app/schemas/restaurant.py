from pydantic import BaseModel, ConfigDict

class RestaurantBase(BaseModel):
    name: str
    address: str

class RestaurantCreate(RestaurantBase):
    """Schema za kreiranje novog restorana."""
    owner_id: int

class RestaurantRead(RestaurantBase):
    """Schema za povratne podatke o restoranu."""
    id: int
    is_active: bool
    owner_id: int

    # Omogućuje Pydanticu da čita podatke iz SQLAlchemy modela
    model_config = ConfigDict(from_attributes=True)

class RestaurantUpdate(BaseModel):
    """Schema za djelomično ažuriranje restorana."""
    name: str | None = None
    address: str | None = None
    is_active: bool | None = None
