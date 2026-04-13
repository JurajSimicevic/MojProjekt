from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, get_current_user, require_role
from app.core.phases import OrderStatus
from app.schemas.order import OrderCreate, OrderRead
from app.services import order_service
from app.repositories import order_repo
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def place_order(
    data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("customer"))
):
    """Kupac kreira novu narudžbu."""
    return await order_repo.create(
        db, 
        customer_id=current_user.id, 
        restaurant_id=data.restaurant_id, 
        item_ids=data.item_ids
    )

@router.get("/my", response_model=list[OrderRead])
async def get_my_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Dohvati povijest narudžbi za trenutnog korisnika (Kupac/Dostavljač/Restoran)."""
    return await order_repo.get_all_for_user(db, current_user)

@router.patch("/{order_id}/status", response_model=OrderRead)
async def change_order_status(
    order_id: int,
    new_status: OrderStatus,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Promjena statusa narudžbe.
    Service sloj provodi state-machine pravila i provjerava uloge.
    """
    order = await order_repo.get_by_id(db, order_id)
    if not order:
        from app.core.errors import AppError
        raise AppError("not_found", "Narudžba ne postoji", 404)

    updated_order = await order_service.update_order_status(
        order, 
        new_status, 
        user_role=current_user.role
    )
    return updated_order
