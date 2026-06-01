from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.restaurant import Restaurant


async def get_all(db: AsyncSession) -> list[Restaurant]:
    result = await db.execute(select(Restaurant).where(Restaurant.is_active.is_(True)))
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, restaurant_id: int) -> Restaurant | None:
    return await db.get(Restaurant, restaurant_id)


async def get_by_owner_id(db: AsyncSession, owner_id: int) -> Restaurant | None:
    result = await db.execute(select(Restaurant).where(Restaurant.owner_id == owner_id))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, name: str, address: str, owner_id: int) -> Restaurant:
    restaurant = Restaurant(name=name, address=address, owner_id=owner_id)
    db.add(restaurant)
    await db.flush()
    await db.refresh(restaurant)
    return restaurant
