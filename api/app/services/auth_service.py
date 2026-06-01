# =============================================================
# auth_service.py — Poslovna logika za autentikaciju
# =============================================================

from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.core.jwt import create_access_token, create_refresh_token, decode_token
from app.core.security import verify_password
from app.models.user import User
from app.repositories import restaurant_repo, user_repo


async def authenticate_user(db: AsyncSession, username: str, password: str) -> User:
    user = await user_repo.get_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        raise AppError("invalid_credentials", "Pogrešno korisničko ime ili lozinka", 401)
    if not user.is_active:
        raise AppError("invalid_credentials", "Korisnički račun je deaktiviran", 401)
    return user


async def create_tokens(db: AsyncSession, user: User) -> tuple[str, str]:
    restaurant_id = None
    if user.role == "restaurant":
        restaurant = await restaurant_repo.get_by_owner_id(db, user.id)
        if restaurant:
            restaurant_id = restaurant.id

    access = create_access_token(user.id, user.role, restaurant_id)
    refresh = create_refresh_token(user.id)
    return access, refresh


async def refresh_tokens(db: AsyncSession, refresh_token: str) -> tuple[str, str]:
    try:
        payload = decode_token(refresh_token)
    except JWTError:
        raise AppError("invalid_credentials", "Nevažeći refresh token", 401)

    if payload.get("type") != "refresh":
        raise AppError("invalid_credentials", "Token nije refresh tipa", 401)

    user = await user_repo.get_by_id(db, int(payload["sub"]))
    if not user or not user.is_active:
        raise AppError("invalid_credentials", "Korisnik ne postoji ili je deaktiviran", 401)

    return await create_tokens(db, user)
