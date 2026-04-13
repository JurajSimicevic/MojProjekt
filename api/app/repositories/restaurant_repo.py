from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.restaurant import Restaurant

async def get_all(db: AsyncSession) -> list[Restaurant]:
    """Dohvati sve aktivne restorane."""
    result = await db.execute(
        select(Restaurant).where(Restaurant.is_active == True)
    )
    return list(result.scalars().all())

async def get_by_id(db: AsyncSession, restaurant_id: int) -> Restaurant | None:
    """Dohvati restoran po ID-u."""
    result = await db.execute(
        select(Restaurant).where(Restaurant.id == restaurant_id)
    )
    return result.scalar_one_or_none()

async def get_by_owner_id(db: AsyncSession, owner_id: int) -> Restaurant | None:
    """Dohvati restoran prema ID-u vlasnika."""
    result = await db.execute(
        select(Restaurant).where(Restaurant.owner_id == owner_id)
    )
    return result.scalar_one_or_none()

async def create(db: AsyncSession, name: str, address: str, owner_id: int) -> Restaurant:
    """Kreiraj novi restoran u bazi."""
    new_restaurant = Restaurant(
        name=name,
        address=address,
        owner_id=owner_id
    )
    db.add(new_restaurant)
    # Napomena: commit se radi automatski u deps.py get_db() yield bloku
    await db.flush() # Flushamo da dobijemo ID nazad
    await db.refresh(new_restaurant)
    return new_restaurant
