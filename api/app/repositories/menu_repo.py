from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.menu_item import MenuItem

async def get_by_restaurant(db: AsyncSession, restaurant_id: int) -> list[MenuItem]:
    """Dohvati sve stavke jelovnika za određeni restoran."""
    result = await db.execute(
        select(MenuItem).where(MenuItem.restaurant_id == restaurant_id)
    )
    return list(result.scalars().all())

async def create(db: AsyncSession, name: str, price: float, restaurant_id: int) -> MenuItem:
    """Dodaj novo jelo na jelovnik."""
    new_item = MenuItem(
        name=name,
        price=price,
        restaurant_id=restaurant_id
    )
    db.add(new_item)
    await db.flush()
    await db.refresh(new_item)
    return new_item

async def update_availability(db: AsyncSession, item_id: int, is_available: bool) -> MenuItem | None:
    """Promijeni dostupnost jela (npr. ako je nestalo sastojaka)."""
    await db.execute(
        update(MenuItem).where(MenuItem.id == item_id).values(is_available=is_available)
    )
    return await db.get(MenuItem, item_id)
