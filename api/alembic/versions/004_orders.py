"""add orders and order items

Revision ID: 004
Revises: 003
Create Date: 2026-05-31
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("customer_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "restaurant_id", sa.Integer(), sa.ForeignKey("restaurants.id"), nullable=False
        ),
        sa.Column("courier_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("total_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column(
            "menu_item_id", sa.Integer(), sa.ForeignKey("menu_items.id"), nullable=False
        ),
        sa.Column("item_name", sa.String(length=100), nullable=False),
        sa.Column("price_at_purchase", sa.Numeric(10, 2), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("order_items")
    op.drop_table("orders")
