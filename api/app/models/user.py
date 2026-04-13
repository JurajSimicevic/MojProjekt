# =============================================================
# user.py — User ORM model
# =============================================================
# Korisnik sustava — kupac, vlasnik restorana, dostavljač ili admin.
#
# Role:
#   "customer"   — naručuje hranu
#   "restaurant" — upravlja jelovnikom i narudžbama
#   "courier"    — dostavlja narudžbe
#   "admin"      — upravlja sustavom
#
# Dizajnerske odluke:
#   - Uklonjen club_id jer restorani imaju vlastiti model
# =============================================================

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    """
    Korisnik sustava.

    Atributi:
        id:            Surrogate primary key.
        username:      Login korisničko ime (jedinstven u sustavu).
        password_hash: Bcrypt hash lozinke (NIKAD plain text).
        role:          "customer", "restaurant", "courier", "admin".
        is_active:     Može li se korisnik prijaviti.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
