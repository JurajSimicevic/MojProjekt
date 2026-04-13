from sqlalchemy.ext.asyncio import AsyncSession
from app.core.errors import AppError
from app.core.jwt import create_access_token, create_refresh_token, decode_token
from app.repositories import user_repo, restaurant_repo
from app.services.user_service import verify_password
from app.models.user import User

async def authenticate(db: AsyncSession, username: str, password: str) -> User:
    """Provjera kredencijala korisnika."""
    user = await user_repo.get_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        raise AppError("invalid_credentials", "Neispravno korisničko ime ili lozinka", 401)
    if not user.is_active:
        raise AppError("invalid_credentials", "Korisnički račun je deaktiviran", 401)
    return user

async def create_tokens(db: AsyncSession, user: User) -> tuple[str, str]:
    """Kreiranje para tokena (access + refresh)."""
    restaurant_id = None
    
    # Ako je korisnik vlasnik restorana, dohvaćamo ID njegovog restorana za JWT payload
    if user.role == "restaurant":
        restaurant = await restaurant_repo.get_by_owner_id(db, user.id)
        if restaurant:
            restaurant_id = restaurant.id
    
    access = create_access_token(user.id, user.role, restaurant_id)
    refresh = create_refresh_token(user.id)
    return access, refresh

async def refresh_tokens(db: AsyncSession, refresh_token: str) -> tuple[str, str]:
    """Izdavanje novih tokena na temelju refresh tokena."""
    try:
        payload = decode_token(refresh_token)
    except Exception:
        raise AppError("invalid_credentials", "Neispravan refresh token", 401)
    
    if payload.get("type") != "refresh":
        raise AppError("invalid_credentials", "Token nije refresh tipa", 401)
    
    user_id = int(payload["sub"])
    user = await user_repo.get_by_id(db, user_id)
    
    if not user or not user.is_active:
        raise AppError("invalid_credentials", "Korisnik ne postoji ili je neaktivan", 401)
    
    return await create_tokens(db, user)
