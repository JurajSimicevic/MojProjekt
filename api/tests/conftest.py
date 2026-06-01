from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.core.deps import get_db
from app.core.security import hash_password
from app.main import app as fastapi_app
from app.models.menu_item import MenuItem
from app.models.restaurant import Restaurant
from app.models.user import User

engine_test = create_async_engine(
    "sqlite+aiosqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = async_sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)


async def _override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


fastapi_app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture(autouse=True)
async def setup_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def admin_user(db: AsyncSession) -> User:
    user = User(
        username="testadmin",
        password_hash=hash_password("admin123"),
        role="admin",
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture
async def customer_user(db: AsyncSession) -> User:
    user = User(
        username="testcustomer",
        password_hash=hash_password("pass123"),
        role="customer",
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture
async def restaurant_user(db: AsyncSession) -> tuple[User, Restaurant, list[MenuItem]]:
    user = User(
        username="testres",
        password_hash=hash_password("pass123"),
        role="restaurant",
        is_active=True,
    )
    db.add(user)
    await db.flush()

    restaurant = Restaurant(name="Test Restoran", address="Adresa 1", owner_id=user.id)
    db.add(restaurant)
    await db.flush()

    items = [
        MenuItem(name="Burger", price=10.0, restaurant_id=restaurant.id),
        MenuItem(name="Pomfrit", price=4.0, restaurant_id=restaurant.id),
    ]
    db.add_all(items)
    await db.commit()
    for item in items:
        await db.refresh(item)
    await db.refresh(user)
    await db.refresh(restaurant)
    return user, restaurant, items


@pytest.fixture
async def courier_user(db: AsyncSession) -> User:
    user = User(
        username="testcourier",
        password_hash=hash_password("pass123"),
        role="courier",
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture
async def inactive_user(db: AsyncSession) -> User:
    user = User(
        username="inactive",
        password_hash=hash_password("pass123"),
        role="admin",
        is_active=False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def auth_header(client: AsyncClient, username: str, password: str) -> dict:
    resp = await client.post("/auth/login", json={"username": username, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
