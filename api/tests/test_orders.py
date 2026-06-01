from httpx import AsyncClient

from app.core.phases import OrderStatus
from app.models.order import Order
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from tests.conftest import auth_header


async def test_place_order_as_customer(
    client: AsyncClient, customer_user, restaurant_user
):
    _, restaurant, items = restaurant_user
    headers = await auth_header(client, "testcustomer", "pass123")

    resp = await client.post(
        "/orders/",
        json={"restaurant_id": restaurant.id, "item_ids": [items[0].id, items[1].id]},
        headers=headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == OrderStatus.PENDING
    assert len(data["items"]) == 2
    assert data["total_price"] == 14.0


async def test_place_order_duplicate_items_counts_quantity(
    client: AsyncClient, customer_user, restaurant_user
):
    _, restaurant, items = restaurant_user
    headers = await auth_header(client, "testcustomer", "pass123")

    resp = await client.post(
        "/orders/",
        json={"restaurant_id": restaurant.id, "item_ids": [items[0].id, items[0].id]},
        headers=headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert len(data["items"]) == 2
    assert data["total_price"] == 20.0


async def test_place_order_inactive_restaurant(
    client: AsyncClient, customer_user, restaurant_user, db: AsyncSession
):
    _, restaurant, items = restaurant_user
    restaurant.is_active = False
    await db.commit()

    headers = await auth_header(client, "testcustomer", "pass123")
    resp = await client.post(
        "/orders/",
        json={"restaurant_id": restaurant.id, "item_ids": [items[0].id]},
        headers=headers,
    )
    assert resp.status_code == 400
    assert resp.json()["code"] == "unavailable"


async def test_invalid_status_transition(
    client: AsyncClient, restaurant_user, customer_user, db: AsyncSession
):
    _, restaurant, _ = restaurant_user
    order = Order(
        customer_id=customer_user.id,
        restaurant_id=restaurant.id,
        total_price=10.0,
        status=OrderStatus.PENDING,
    )
    db.add(order)
    await db.commit()

    headers = await auth_header(client, "testres", "pass123")
    resp = await client.patch(
        f"/orders/{order.id}/status",
        params={"new_status": OrderStatus.READY.value},
        headers=headers,
    )

    assert resp.status_code == 400
    assert resp.json()["code"] == "invalid_transition"


async def test_role_restricted_status_update(
    client: AsyncClient, customer_user, restaurant_user, db: AsyncSession
):
    _, restaurant, _ = restaurant_user
    order = Order(
        customer_id=customer_user.id,
        restaurant_id=restaurant.id,
        total_price=10.0,
        status=OrderStatus.PENDING,
    )
    db.add(order)
    await db.commit()

    headers = await auth_header(client, "testcustomer", "pass123")
    resp = await client.patch(
        f"/orders/{order.id}/status",
        params={"new_status": OrderStatus.ACCEPTED.value},
        headers=headers,
    )

    assert resp.status_code == 403
    assert resp.json()["code"] == "forbidden"


async def test_customer_can_cancel_pending_order(
    client: AsyncClient, customer_user, restaurant_user, db: AsyncSession
):
    _, restaurant, _ = restaurant_user
    order = Order(
        customer_id=customer_user.id,
        restaurant_id=restaurant.id,
        total_price=10.0,
        status=OrderStatus.PENDING,
    )
    db.add(order)
    await db.commit()

    headers = await auth_header(client, "testcustomer", "pass123")
    resp = await client.patch(
        f"/orders/{order.id}/status",
        params={"new_status": OrderStatus.CANCELLED.value},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == OrderStatus.CANCELLED


async def test_courier_sees_ready_unassigned_orders(
    client: AsyncClient, courier_user, customer_user, restaurant_user, db: AsyncSession
):
    _, restaurant, _ = restaurant_user
    order = Order(
        customer_id=customer_user.id,
        restaurant_id=restaurant.id,
        total_price=10.0,
        status=OrderStatus.READY,
    )
    db.add(order)
    await db.commit()

    headers = await auth_header(client, "testcourier", "pass123")
    resp = await client.get("/orders/my", headers=headers)
    assert resp.status_code == 200
    assert any(o["id"] == order.id for o in resp.json())


async def test_wrong_courier_cannot_deliver(
    client: AsyncClient, courier_user, customer_user, restaurant_user, db: AsyncSession
):
    _, restaurant, _ = restaurant_user

    other_courier = User(
        username="othercourier",
        password_hash=hash_password("pass123"),
        role="courier",
        is_active=True,
    )
    db.add(other_courier)
    await db.flush()

    order = Order(
        customer_id=customer_user.id,
        restaurant_id=restaurant.id,
        total_price=10.0,
        status=OrderStatus.ON_THE_WAY,
        courier_id=other_courier.id,
    )
    db.add(order)
    await db.commit()

    headers = await auth_header(client, "testcourier", "pass123")
    resp = await client.patch(
        f"/orders/{order.id}/status",
        params={"new_status": OrderStatus.DELIVERED.value},
        headers=headers,
    )
    assert resp.status_code == 403


async def test_get_order_by_id(
    client: AsyncClient, customer_user, restaurant_user
):
    _, restaurant, items = restaurant_user
    headers = await auth_header(client, "testcustomer", "pass123")

    create_resp = await client.post(
        "/orders/",
        json={"restaurant_id": restaurant.id, "item_ids": [items[0].id]},
        headers=headers,
    )
    order_id = create_resp.json()["id"]

    resp = await client.get(f"/orders/{order_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == order_id
    assert len(resp.json()["items"]) == 1


async def test_get_my_orders_unauthenticated(client: AsyncClient):
    resp = await client.get("/orders/my")
    assert resp.status_code == 401


async def test_inactive_restaurant_not_publicly_visible(
    client: AsyncClient, restaurant_user, db: AsyncSession
):
    _, restaurant, _ = restaurant_user
    restaurant.is_active = False
    await db.commit()

    resp = await client.get(f"/restaurants/{restaurant.id}")
    assert resp.status_code == 404
