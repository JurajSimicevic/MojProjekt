from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_role
from app.schemas.user import UserCreate, UserRead
from app.services import user_service
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_customer(data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Javna registracija za nove kupce."""
    return await user_service.register_user(
        db, username=data.username, password=data.password, role="customer"
    )

@router.post("/staff", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_staff(
    data: UserCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    """
    Samo admin može kreirati vlasnike restorana ili dostavljače.
    'role' u bodyju mora biti 'restaurant' ili 'courier'.
    """
    return await user_service.register_user(
        db, username=data.username, password=data.password, role=data.role
    )
