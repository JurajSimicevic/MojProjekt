import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import engine, Base, AsyncSessionLocal
from app.core.security import hash_password
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def setup():
    try:
        logger.info("Kreiranje tablica u bazi...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        logger.info("Seeding početnih podataka...")
        async with AsyncSessionLocal() as db:
            # 1. Admin
            admin = User(username="admin", password_hash=hash_password("admin123"), role="admin")
            # 2. Vlasnik restorana
            owner = User(username="owner", password_hash=hash_password("owner123"), role="restaurant")
            # 3. Kupac
            customer = User(username="customer", password_hash=hash_password("customer123"), role="customer")
            
            db.add_all([admin, owner, customer])
            await db.flush()

            # 4. Restoran
            res = Restaurant(name="Pizzeria Test", address="Ulica 1", owner_id=owner.id)
            db.add(res)
            await db.flush()

            # 5. Menu Items
            m1 = MenuItem(name="Margherita", price=8.50, restaurant_id=res.id)
            m2 = MenuItem(name="Pepperoni", price=10.00, restaurant_id=res.id)
            db.add_all([m1, m2])
            
            await db.commit()
        
        logger.info("Baza je spremna!")
    except Exception as e:
        logger.error(f"Greška pri postavljanju baze: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(setup())