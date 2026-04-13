from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    """Schema za registraciju novog korisnika."""
    password: str

class UserRead(UserBase):
    """Schema za povratne podatke o korisniku."""
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
