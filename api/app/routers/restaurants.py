from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_role
from app.models.user import User
from app.schemas.restaurant import RestaurantCreate, RestaurantRead
from app.services import restaurant_service

router = APIRouter()


@router.get("/", response_model=list[RestaurantRead])
async def list_restaurants(db: AsyncSession = Depends(get_db)):
    return await restaurant_service.list_active_restaurants(db)


@router.post("/", response_model=RestaurantRead, status_code=status.HTTP_201_CREATED)
async def create_restaurant(
    data: RestaurantCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role("admin")),
):
    return await restaurant_service.create_restaurant(
        db, name=data.name, address=data.address, owner_id=data.owner_id
    )


@router.get("/{restaurant_id}", response_model=RestaurantRead)
async def get_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await restaurant_service.get_restaurant(db, restaurant_id, active_only=True)
