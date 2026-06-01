# =============================================================
# restaurant_service.py — Poslovna logika za restorane
# =============================================================

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.models.restaurant import Restaurant
from app.models.user import User
from app.repositories import restaurant_repo, user_repo


async def _get_or_404(db: AsyncSession, restaurant_id: int) -> Restaurant:
    restaurant = await restaurant_repo.get_by_id(db, restaurant_id)
    if not restaurant:
        raise AppError("not_found", "Restoran ne postoji", 404)
    return restaurant


def verify_restaurant_ownership(restaurant: Restaurant, user: User) -> None:
    if user.role == "admin":
        return
    if restaurant.owner_id != user.id:
        raise AppError("forbidden", "Niste vlasnik ovog restorana", 403)


async def list_active_restaurants(db: AsyncSession) -> list[Restaurant]:
    return await restaurant_repo.get_all(db)


async def get_restaurant(
    db: AsyncSession, restaurant_id: int, *, active_only: bool = False
) -> Restaurant:
    restaurant = await _get_or_404(db, restaurant_id)
    if active_only and not restaurant.is_active:
        raise AppError("not_found", "Restoran ne postoji", 404)
    return restaurant


async def create_restaurant(
    db: AsyncSession, name: str, address: str, owner_id: int
) -> Restaurant:
    owner = await user_repo.get_by_id(db, owner_id)
    if not owner:
        raise AppError("not_found", "Vlasnik ne postoji", 404)
    if owner.role not in ("restaurant", "admin"):
        raise AppError("validation_error", "Vlasnik mora imati ulogu restaurant", 400)

    existing = await restaurant_repo.get_by_owner_id(db, owner_id)
    if existing:
        raise AppError("duplicate", "Korisnik već ima restoran", 409)

    return await restaurant_repo.create(db, name, address, owner_id)


async def get_owned_restaurant(db: AsyncSession, user: User) -> Restaurant | None:
    if user.role != "restaurant":
        return None
    return await restaurant_repo.get_by_owner_id(db, user.id)
