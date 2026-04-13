# Označava "repositories" kao Python paket.
from . import user_repo, restaurant_repo, menu_repo, order_repo

__all__ = ["user_repo", "restaurant_repo", "menu_repo", "order_repo"]
