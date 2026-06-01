# =============================================================
# menu_service.py — Poslovna logika za jelovnik
# =============================================================

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.models.menu_item import MenuItem
from app.models.user import User
from app.repositories import menu_repo
from app.services import restaurant_service


async def list_menu(
    db: AsyncSession, restaurant_id: int, *, available_only: bool = True
) -> list[MenuItem]:
    await restaurant_service.get_restaurant(db, restaurant_id, active_only=available_only)
    items = await menu_repo.get_by_restaurant(db, restaurant_id)
    if available_only:
        return [item for item in items if item.is_available]
    return items


async def add_menu_item(
    db: AsyncSession,
    restaurant_id: int,
    user: User,
    name: str,
    price: float,
    description: str | None = None,
) -> MenuItem:
    restaurant = await restaurant_service.get_restaurant(db, restaurant_id)
    restaurant_service.verify_restaurant_ownership(restaurant, user)
    return await menu_repo.create(
        db, name=name, price=price, restaurant_id=restaurant_id, description=description
    )


async def set_item_availability(
    db: AsyncSession, item_id: int, user: User, is_available: bool
) -> MenuItem:
    item = await menu_repo.get_by_id(db, item_id)
    if not item:
        raise AppError("not_found", "Stavka jelovnika ne postoji", 404)

    restaurant = await restaurant_service.get_restaurant(db, item.restaurant_id)
    restaurant_service.verify_restaurant_ownership(restaurant, user)

    updated = await menu_repo.update_availability(db, item_id, is_available)
    assert updated is not None
    return updated
