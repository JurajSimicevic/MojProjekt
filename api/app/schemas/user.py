from pydantic import BaseModel, ConfigDict, Field


class CustomerRegister(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1)


class StaffCreate(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1)
    role: str = Field(description="restaurant ili courier")


class UserRead(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
