import pytest
from httpx import AsyncClient
from app.core.phases import OrderStatus
from app.models.order import Order
from sqlalchemy.ext.asyncio import AsyncSession
from tests.conftest import auth_header

@pytest.mark.asyncio
async def test_place_order_as_customer(client: AsyncClient, customer_user):
    """Provjera da kupac može kreirati narudžbu."""
    headers = await auth_header(client, "testcustomer", "pass123")
    
    order_data = {
        "restaurant_id": 1,
        "item_ids": [1, 2]
    }
    
    resp = await client.post("/orders/", json=order_data, headers=headers)
    assert resp.status_code == 201
    assert resp.json()["status"] == OrderStatus.PENDING

@pytest.mark.asyncio
async def test_invalid_status_transition(client: AsyncClient, restaurant_user, customer_user, db: AsyncSession):
    """Provjera da se ne može preskočiti status (npr. PENDING -> READY)."""
    # Kreiramo narudžbu direktno u bazi kako bismo imali što testirati
    order = Order(customer_id=customer_user.id, restaurant_id=1, total_price=10.0, status=OrderStatus.PENDING)
    db.add(order)
    await db.commit()

    headers = await auth_header(client, "testres", "pass123")
    
    # Pokušaj promjene s PENDING direktno na READY (mora baciti 400)
    resp = await client.patch(
        f"/orders/{order.id}/status", 
        params={"new_status": OrderStatus.READY.value}, 
        headers=headers
    )
    
    assert resp.status_code == 400
    assert resp.json()["code"] == "invalid_transition"

@pytest.mark.asyncio
async def test_role_restricted_status_update(client: AsyncClient, customer_user, db: AsyncSession):
    """Provjera da kupac ne može 'prihvatiti' vlastitu narudžbu."""
    # Kreiramo narudžbu
    order = Order(customer_id=customer_user.id, restaurant_id=1, total_price=10.0, status=OrderStatus.PENDING)
    db.add(order)
    await db.commit()

    headers = await auth_header(client, "testcustomer", "pass123")
    
    resp = await client.patch(
        f"/orders/{order.id}/status", 
        params={"new_status": OrderStatus.ACCEPTED.value}, 
        headers=headers
    )
    
    assert resp.status_code == 403
    assert resp.json()["code"] == "forbidden"

@pytest.mark.asyncio
async def test_get_my_orders_unauthenticated(client: AsyncClient):
    """Provjera da neautenticirani korisnik ne vidi narudžbe."""
    resp = await client.get("/orders/my")
    assert resp.status_code == 401
