# =============================================================
# user_repo.py — DB upiti za User model
# =============================================================

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
    """Dohvati korisnika po primarnom ključu."""
    return await db.get(User, user_id)

async def get_by_username(db: AsyncSession, username: str) -> User | None:
    """Dohvati korisnika po username-u (za login)."""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def create(db: AsyncSession, username: str, password_hash: str, role: str) -> User:
    """Spremi novog korisnika u bazu."""
    new_user = User(
        username=username,
        password_hash=password_hash,
        role=role
    )
    db.add(new_user)
    await db.flush()
    await db.refresh(new_user)
    return new_user
