from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.user import User
from app.models.menu_item import MenuItem

async def create(db: AsyncSession, customer_id: int, restaurant_id: int, item_ids: list[int]) -> Order:
    """Kreiraj novu narudžbu."""
    # Dohvati cijene jela iz baze (sigurnost!)
    result = await db.execute(select(MenuItem).where(MenuItem.id.in_(item_ids)))
    items = result.scalars().all()
    
    calculated_total = sum(item.price for item in items)

    new_order = Order(
        customer_id=customer_id,
        restaurant_id=restaurant_id,
        total_price=calculated_total
    )
    db.add(new_order)
    await db.flush() # Dobivamo ID narudžbe

    # Spremi stavke narudžbe
    for item in items:
        oi = OrderItem(
            order_id=new_order.id,
            menu_item_id=item.id,
            item_name=item.name,
            price_at_purchase=item.price
        )
        db.add(oi)

    await db.flush()
    await db.refresh(new_order)
    return new_order

async def get_by_id(db: AsyncSession, order_id: int) -> Order | None:
    """Dohvati narudžbu po ID-u."""
    return await db.get(Order, order_id)

async def get_all_for_user(db: AsyncSession, user: User) -> list[Order]:
    """
    Dohvati listu narudžbi ovisno o ulozi korisnika.
    Kupac vidi svoje, dostavljač one koje dostavlja, restoran svoje dolazne.
    """
    query = select(Order)
    
    if user.role == "customer":
        query = query.where(Order.customer_id == user.id)
    elif user.role == "courier":
        query = query.where(Order.courier_id == user.id)
    elif user.role == "restaurant":
        # Napomena: Ovdje bi u stvarnosti išao JOIN na Restaurant 
        # da se provjeri ownership, za sada filtriramo po restaurant_id.
        query = query.where(Order.restaurant_id == user.id)
        
    query = query.order_by(Order.created_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())
