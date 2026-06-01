from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_role
from app.models.user import User
from app.schemas.menu_item import MenuItemCreate, MenuItemRead
from app.services import menu_service

router = APIRouter()


@router.get("/restaurants/{restaurant_id}/items", response_model=list[MenuItemRead])
async def get_restaurant_menu(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await menu_service.list_menu(db, restaurant_id)


@router.post("/items", response_model=MenuItemRead, status_code=status.HTTP_201_CREATED)
async def add_menu_item(
    data: MenuItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("restaurant", "admin")),
):
    return await menu_service.add_menu_item(
        db,
        restaurant_id=data.restaurant_id,
        user=current_user,
        name=data.name,
        price=data.price,
        description=data.description,
    )


@router.patch("/items/{item_id}/availability", response_model=MenuItemRead)
async def toggle_item_availability(
    item_id: int,
    is_available: bool,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("restaurant", "admin")),
):
    return await menu_service.set_item_availability(
        db, item_id=item_id, user=current_user, is_available=is_available
    )
