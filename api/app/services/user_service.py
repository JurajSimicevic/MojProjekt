from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.errors import AppError
from app.repositories import user_repo
from app.models.user import User

# Inicijalizacija passlib contexta za bcrypt.
# Na novijim verzijama Pythona (3.13+), osigurajte da je instaliran 'bcrypt' paket.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def register_user(db: AsyncSession, username: str, password: str, role: str) -> User:
    """
    Poslovna logika za registraciju: provjera jedinstvenosti i hashiranje.
    """
    existing = await user_repo.get_by_username(db, username)
    if existing:
        raise AppError("username_taken", "Korisničko ime je zauzeto", 400)
    
    hashed = hash_password(password)
    return await user_repo.create(
        db, 
        username=username, 
        password_hash=hashed, 
        role=role
    )
