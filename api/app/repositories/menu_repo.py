from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.menu_item import MenuItem


async def get_by_id(db: AsyncSession, item_id: int) -> MenuItem | None:
    return await db.get(MenuItem, item_id)


async def get_by_restaurant(db: AsyncSession, restaurant_id: int) -> list[MenuItem]:
    result = await db.execute(
        select(MenuItem).where(MenuItem.restaurant_id == restaurant_id)
    )
    return list(result.scalars().all())


async def create(
    db: AsyncSession,
    name: str,
    price: float,
    restaurant_id: int,
    description: str | None = None,
) -> MenuItem:
    item = MenuItem(
        name=name,
        price=price,
        restaurant_id=restaurant_id,
        description=description,
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


async def update_availability(
    db: AsyncSession, item_id: int, is_available: bool
) -> MenuItem | None:
    await db.execute(
        update(MenuItem).where(MenuItem.id == item_id).values(is_available=is_available)
    )
    return await db.get(MenuItem, item_id)
