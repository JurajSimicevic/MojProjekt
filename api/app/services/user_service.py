# =============================================================
# user_service.py — Poslovna logika za korisnike
# =============================================================

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.core.security import hash_password
from app.models.user import User
from app.repositories import user_repo

ALLOWED_STAFF_ROLES = {"restaurant", "courier"}


async def register_customer(db: AsyncSession, username: str, password: str) -> User:
    return await _register(db, username, password, "customer")


async def create_staff_user(
    db: AsyncSession, username: str, password: str, role: str
) -> User:
    if role not in ALLOWED_STAFF_ROLES:
        raise AppError(
            "validation_error",
            "Uloga mora biti 'restaurant' ili 'courier'",
            400,
        )
    return await _register(db, username, password, role)


async def _register(db: AsyncSession, username: str, password: str, role: str) -> User:
    existing = await user_repo.get_by_username(db, username)
    if existing:
        raise AppError("username_taken", "Korisničko ime je zauzeto", 400)

    return await user_repo.create(
        db,
        username=username,
        password_hash=hash_password(password),
        role=role,
    )
