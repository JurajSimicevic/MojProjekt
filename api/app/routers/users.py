from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_role
from app.models.user import User
from app.schemas.user import CustomerRegister, StaffCreate, UserRead
from app.services import user_service

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_customer(data: CustomerRegister, db: AsyncSession = Depends(get_db)):
    return await user_service.register_customer(
        db, username=data.username, password=data.password
    )


@router.post("/staff", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_staff(
    data: StaffCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role("admin")),
):
    return await user_service.create_staff_user(
        db, username=data.username, password=data.password, role=data.role
    )
