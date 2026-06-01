# =============================================================
# seed.py — Inicijalni podaci za razvoj i testiranje
# =============================================================

import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal, engine
from app.core.security import hash_password
from app.models.menu_item import MenuItem
from app.models.restaurant import Restaurant
from app.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

RESTAURANTS = [
    {
        "username": "pizza_owner",
        "password": "rest123",
        "restaurant_name": "Pizza Place",
        "address": "Ilica 1, Zagreb",
        "menu": [
            {"name": "Margherita", "price": 9.99, "description": "Sir i rajčica"},
            {"name": "Capricciosa", "price": 11.99, "description": "Šunka i gljive"},
        ],
    },
    {
        "username": "burger_owner",
        "password": "rest123",
        "restaurant_name": "Burger House",
        "address": "Vukovarska 10, Zagreb",
        "menu": [
            {"name": "Classic Burger", "price": 8.50, "description": "Govedina i salata"},
            {"name": "Cheese Burger", "price": 9.50, "description": "Govedina i sir"},
        ],
    },
]

CUSTOMER = {"username": "customer1", "password": "cust123"}
COURIER = {"username": "courier1", "password": "cour123"}


async def _ensure_user(
    session: AsyncSession, username: str, password: str, role: str
) -> User:
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(
            username=username,
            password_hash=hash_password(password),
            role=role,
            is_active=True,
        )
        session.add(user)
        await session.flush()
        logger.info("Kreiran korisnik: %s (%s)", username, role)
    return user


async def _seed_restaurant(session: AsyncSession, data: dict) -> None:
    user = await _ensure_user(
        session, data["username"], data["password"], "restaurant"
    )

    result = await session.execute(
        select(Restaurant).where(Restaurant.owner_id == user.id)
    )
    restaurant = result.scalar_one_or_none()
    if restaurant is None:
        restaurant = Restaurant(
            name=data["restaurant_name"],
            address=data["address"],
            owner_id=user.id,
        )
        session.add(restaurant)
        await session.flush()
        logger.info("Kreiran restoran: %s", restaurant.name)

    for item_data in data["menu"]:
        result = await session.execute(
            select(MenuItem).where(
                MenuItem.restaurant_id == restaurant.id,
                MenuItem.name == item_data["name"],
            )
        )
        if result.scalar_one_or_none() is None:
            session.add(
                MenuItem(
                    name=item_data["name"],
                    description=item_data.get("description"),
                    price=item_data["price"],
                    restaurant_id=restaurant.id,
                )
            )
            logger.info("Dodana stavka: %s (%s)", item_data["name"], restaurant.name)


async def seed(session: AsyncSession) -> None:
    await _ensure_user(session, ADMIN_USERNAME, ADMIN_PASSWORD, "admin")
    await _ensure_user(session, CUSTOMER["username"], CUSTOMER["password"], "customer")
    await _ensure_user(session, COURIER["username"], COURIER["password"], "courier")

    for restaurant_data in RESTAURANTS:
        await _seed_restaurant(session, restaurant_data)

    await session.commit()
    logger.info("Seed završen uspješno!")


async def main() -> None:
    async with AsyncSessionLocal() as session:
        await seed(session)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
