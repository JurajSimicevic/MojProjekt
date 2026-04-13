from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, get_current_user, require_role
from app.schemas.menu_item import MenuItemCreate, MenuItemRead
from app.services import menu_service
from app.repositories import menu_repo
from app.models.user import User

router = APIRouter()

@router.get("/restaurants/{restaurant_id}/items", response_model=list[MenuItemRead])
async def get_restaurant_menu(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    """Javni dohvat jelovnika za određeni restoran."""
    return await menu_repo.get_by_restaurant(db, restaurant_id)

@router.post("/items", response_model=MenuItemRead, status_code=status.HTTP_201_CREATED)
async def add_menu_item(
    data: MenuItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("restaurant", "admin"))
):
    """
    Dodavanje novog jela na jelovnik. 
    Service sloj provjerava je li korisnik vlasnik restorana.
    """
    item_dict = data.model_dump()
    return await menu_service.add_item_to_menu(
        db, restaurant_id=data.restaurant_id, user=current_user, item_data=item_dict
    )

@router.patch("/items/{item_id}/availability", response_model=MenuItemRead)
async def toggle_item_availability(
    item_id: int,
    is_available: bool,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("restaurant"))
):
    """Vlasnik restorana može uključiti/isključiti jelo iz ponude."""
    # Ovdje bi išao poziv prema repo/service za update is_available
    return await menu_repo.update_availability(db, item_id, is_available)
