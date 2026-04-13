from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_role
from app.schemas.restaurant import RestaurantCreate, RestaurantRead
from app.repositories import restaurant_repo
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[RestaurantRead])
async def list_restaurants(
    db: AsyncSession = Depends(get_db)
):
    """Dohvati listu svih aktivnih restorana."""
    return await restaurant_repo.get_all(db)

@router.post("/", response_model=RestaurantRead, status_code=status.HTTP_201_CREATED)
async def create_restaurant(
    data: RestaurantCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    """
    Kreiraj novi restoran. 
    Samo korisnici s ulogom 'admin' mogu kreirati restorane.
    """
    return await restaurant_repo.create(
        db, 
        name=data.name, 
        address=data.address, 
        owner_id=data.owner_id
    )

@router.get("/{id}", response_model=RestaurantRead)
async def get_restaurant(id: int, db: AsyncSession = Depends(get_db)):
    """Dohvati detalje specifičnog restorana."""
    resp = await restaurant_repo.get_by_id(db, id)
    if not resp:
        from app.core.errors import AppError
        raise AppError("not_found", "Restoran ne postoji", 404)
    return resp
