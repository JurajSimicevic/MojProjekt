from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, get_current_user, require_role
from app.core.phases import OrderStatus
from app.models.user import User
from app.schemas.order import OrderCreate, OrderRead
from app.services import order_service

router = APIRouter()


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def place_order(
    data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("customer")),
):
    return await order_service.place_order(
        db,
        customer_id=current_user.id,
        restaurant_id=data.restaurant_id,
        item_ids=data.item_ids,
    )


@router.get("/my", response_model=list[OrderRead])
async def get_my_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await order_service.list_orders_for_user(db, current_user)


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await order_service.get_order(db, order_id, current_user)


@router.patch("/{order_id}/status", response_model=OrderRead)
async def change_order_status(
    order_id: int,
    new_status: OrderStatus,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await order_service.change_order_status(
        db, order_id=order_id, new_status=new_status, user=current_user
    )
