from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.deps import get_db, get_current_user
from app.schemas.user import UserRead, Token
from app.services import auth_service

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/login", response_model=Token)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Prijava u sustav."""
    user = await auth_service.authenticate(db, data.username, data.password)
    access, refresh = await auth_service.create_tokens(db, user)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
async def refresh(
    data: RefreshRequest,
    db: AsyncSession = Depends(get_db)
):
    """Osvježavanje access tokena."""
    access, refresh = await auth_service.refresh_tokens(db, data.refresh_token)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
async def me(user = Depends(get_current_user)):
    """Dohvat podataka trenutno prijavljenog korisnika."""
    return user
