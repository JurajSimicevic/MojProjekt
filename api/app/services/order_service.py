# =============================================================
# order_service.py — Poslovna logika za narudžbe
# =============================================================

from collections import Counter

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.core.phases import OrderStatus
from app.models.order import Order
from app.models.user import User
from app.repositories import menu_repo, order_repo
from app.services import restaurant_service


def _normalize_status(status: OrderStatus | str) -> OrderStatus:
    if isinstance(status, OrderStatus):
        return status
    return OrderStatus(status)


def validate_status_transition(current: OrderStatus, new: OrderStatus) -> None:
    transitions = {
        OrderStatus.PENDING: [OrderStatus.ACCEPTED, OrderStatus.CANCELLED],
        OrderStatus.ACCEPTED: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
        OrderStatus.PREPARING: [OrderStatus.READY],
        OrderStatus.READY: [OrderStatus.ON_THE_WAY],
        OrderStatus.ON_THE_WAY: [OrderStatus.DELIVERED],
        OrderStatus.DELIVERED: [],
        OrderStatus.CANCELLED: [],
    }
    if new not in transitions.get(current, []):
        raise AppError(
            code="invalid_transition",
            message=f"Nije moguće promijeniti status iz {current} u {new}",
            status_code=400,
        )


def _verify_order_access(order: Order, user: User, restaurant_id: int | None) -> None:
    if user.role == "admin":
        return
    if user.role == "customer" and order.customer_id == user.id:
        return
    if user.role == "restaurant" and restaurant_id and order.restaurant_id == restaurant_id:
        return
    if user.role == "courier" and (
        order.courier_id == user.id
        or (
            order.courier_id is None
            and _normalize_status(order.status) == OrderStatus.READY
        )
    ):
        return
    raise AppError("forbidden", "Nemate pristup ovoj narudžbi", 403)


async def place_order(
    db: AsyncSession, customer_id: int, restaurant_id: int, item_ids: list[int]
) -> Order:
    if not item_ids:
        raise AppError("validation_error", "Narudžba mora sadržavati barem jednu stavku", 400)

    restaurant = await restaurant_service.get_restaurant(db, restaurant_id)
    if not restaurant.is_active:
        raise AppError("unavailable", "Restoran trenutno ne prima narudžbe", 400)

    counts = Counter(item_ids)
    for item_id, qty in counts.items():
        if qty < 1:
            raise AppError("validation_error", "Količina mora biti pozitivna", 400)
        item = await menu_repo.get_by_id(db, item_id)
        if not item or item.restaurant_id != restaurant_id:
            raise AppError("not_found", f"Stavka {item_id} ne postoji u restoranu", 404)
        if not item.is_available:
            raise AppError("unavailable", f"Stavka '{item.name}' nije dostupna", 400)

    return await order_repo.create(db, customer_id, restaurant_id, item_ids)


async def get_order(db: AsyncSession, order_id: int, user: User) -> Order:
    order = await order_repo.get_by_id(db, order_id)
    if not order:
        raise AppError("not_found", "Narudžba ne postoji", 404)

    restaurant_id = None
    if user.role == "restaurant":
        restaurant = await restaurant_service.get_owned_restaurant(db, user)
        restaurant_id = restaurant.id if restaurant else None

    _verify_order_access(order, user, restaurant_id)
    return order


async def list_orders_for_user(db: AsyncSession, user: User) -> list[Order]:
    restaurant_id = None
    if user.role == "restaurant":
        restaurant = await restaurant_service.get_owned_restaurant(db, user)
        restaurant_id = restaurant.id if restaurant else None
    return await order_repo.get_all_for_user(db, user, restaurant_id)


async def change_order_status(
    db: AsyncSession, order_id: int, new_status: OrderStatus, user: User
) -> Order:
    order = await order_repo.get_by_id(db, order_id)
    if not order:
        raise AppError("not_found", "Narudžba ne postoji", 404)

    current = _normalize_status(order.status)

    if user.role == "customer":
        if order.customer_id != user.id:
            raise AppError("forbidden", "Ne možete mijenjati tuđu narudžbu", 403)
        if new_status != OrderStatus.CANCELLED or current != OrderStatus.PENDING:
            raise AppError(
                "forbidden",
                "Kupac može otkazati narudžbu samo dok je u statusu pending",
                403,
            )
    elif user.role == "restaurant":
        restaurant = await restaurant_service.get_owned_restaurant(db, user)
        if not restaurant or order.restaurant_id != restaurant.id:
            raise AppError("forbidden", "Ne možete mijenjati tuđu narudžbu", 403)
        if new_status in (OrderStatus.ON_THE_WAY, OrderStatus.DELIVERED):
            raise AppError("forbidden", "Restoran ne može označiti dostavu", 403)
    elif user.role == "courier":
        if new_status == OrderStatus.ON_THE_WAY:
            if order.courier_id is not None and order.courier_id != user.id:
                raise AppError(
                    "forbidden", "Narudžbu je već preuzeo drugi dostavljač", 403
                )
            order.courier_id = user.id
        elif new_status == OrderStatus.DELIVERED:
            if order.courier_id != user.id:
                raise AppError("forbidden", "Niste dodijeljeni ovoj narudžbi", 403)
        else:
            raise AppError(
                "forbidden",
                "Dostavljač može samo preuzeti (on_the_way) ili dostaviti (delivered) narudžbu",
                403,
            )
    elif user.role != "admin":
        raise AppError("forbidden", "Nemate dozvolu za promjenu statusa", 403)

    validate_status_transition(current, new_status)

    order.status = new_status
    await db.flush()
    return order
