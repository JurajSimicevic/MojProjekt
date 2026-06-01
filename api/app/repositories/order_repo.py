from collections import Counter

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.phases import OrderStatus
from app.models.menu_item import MenuItem
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.user import User


async def create(
    db: AsyncSession, customer_id: int, restaurant_id: int, item_ids: list[int]
) -> Order:
    counts = Counter(item_ids)
    unique_ids = list(counts.keys())

    result = await db.execute(select(MenuItem).where(MenuItem.id.in_(unique_ids)))
    items_by_id = {item.id: item for item in result.scalars().all()}

    total = 0.0
    for item_id, qty in counts.items():
        total += float(items_by_id[item_id].price) * qty

    order = Order(
        customer_id=customer_id,
        restaurant_id=restaurant_id,
        total_price=total,
    )
    db.add(order)
    await db.flush()

    for item_id, qty in counts.items():
        item = items_by_id.get(item_id)
        if item is None:
            raise ValueError(f"Menu item {item_id} not found")
        for _ in range(qty):
            db.add(
                OrderItem(
                    order_id=order.id,
                    menu_item_id=item.id,
                    item_name=item.name,
                    price_at_purchase=item.price,
                )
            )

    await db.flush()
    return await get_by_id(db, order.id)


async def get_by_id(db: AsyncSession, order_id: int) -> Order | None:
    result = await db.execute(
        select(Order).options(selectinload(Order.items)).where(Order.id == order_id)
    )
    return result.scalar_one_or_none()


async def get_all_for_user(db: AsyncSession, user: User, restaurant_id: int | None) -> list[Order]:
    query = select(Order).options(selectinload(Order.items))

    if user.role == "customer":
        query = query.where(Order.customer_id == user.id)
    elif user.role == "courier":
        query = query.where(
            or_(
                Order.courier_id == user.id,
                and_(
                    Order.status == OrderStatus.READY.value,
                    Order.courier_id.is_(None),
                ),
            )
        )
    elif user.role == "restaurant":
        if restaurant_id is None:
            return []
        query = query.where(Order.restaurant_id == restaurant_id)
    elif user.role == "admin":
        pass
    else:
        return []

    query = query.order_by(Order.created_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())
