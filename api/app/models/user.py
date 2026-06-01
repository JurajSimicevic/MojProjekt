# =============================================================
# user.py — User ORM model
# =============================================================

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    """
    Korisnik sustava.

    Role:
      customer   — naručuje hranu
      restaurant — upravlja jelovnikom i narudžbama
      courier    — dostavlja narudžbe
      admin      — upravlja sustavom
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
