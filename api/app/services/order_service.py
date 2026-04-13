from app.core.errors import AppError
from app.core.phases import OrderStatus
from app.models.order import Order

def validate_status_transition(current: OrderStatus, new: OrderStatus):
    """
    Provjerava je li prijelaz iz jednog statusa u drugi dozvoljen.
    Implementira 'State Machine' logiku.
    """
    transitions = {
        OrderStatus.PENDING: [OrderStatus.ACCEPTED, OrderStatus.CANCELLED],
        OrderStatus.ACCEPTED: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
        OrderStatus.PREPARING: [OrderStatus.READY],
        OrderStatus.READY: [OrderStatus.ON_THE_WAY],
        OrderStatus.ON_THE_WAY: [OrderStatus.DELIVERED],
        OrderStatus.DELIVERED: [],  # Finalni status
        OrderStatus.CANCELLED: []   # Finalni status
    }

    if new not in transitions.get(current, []):
        raise AppError(
            code="invalid_transition",
            message=f"Nije moguće promijeniti status iz {current} u {new}",
            status_code=400
        )

async def update_order_status(order: Order, new_status: OrderStatus, user_role: str):
    """
    Poslovna logika za promjenu statusa narudžbe s provjerom ovlasti.
    """
    # 1. Provjeri logiku prijelaza
    validate_status_transition(order.status, new_status)

    # 2. Provjeri tko smije raditi što
    if new_status == OrderStatus.ACCEPTED and user_role != "restaurant":
        raise AppError("forbidden", "Samo restoran može prihvatiti narudžbu", 403)
    
    if new_status == OrderStatus.ON_THE_WAY and user_role != "courier":
        raise AppError("forbidden", "Samo dostavljač može preuzeti narudžbu", 403)

    order.status = new_status
    return order
