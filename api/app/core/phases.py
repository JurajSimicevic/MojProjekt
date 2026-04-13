# =============================================================
# phases.py — Statusi narudžbe (konačni automat)
# =============================================================
# Definira životni ciklus narudžbe:
#   PENDING   -> RESTAURANT_ACCEPTED -> PREPARING -> 
#   READY     -> PICKED_UP           -> DELIVERED
#
# Korištenje u service layeru:
#   if order.status != OrderStatus.READY:
#       raise AppError("invalid_transition", "Order is not ready for pickup")
# =============================================================

from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    PREPARING = "preparing"
    READY = "ready"
    ON_THE_WAY = "on_the_way"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
