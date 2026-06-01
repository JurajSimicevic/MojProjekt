from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.menu_item import MenuItem
    from app.models.user import User


class Restaurant(Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    menu_items: Mapped[list[MenuItem]] = relationship(back_populates="restaurant")
    owner: Mapped[User] = relationship()
