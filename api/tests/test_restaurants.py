from httpx import AsyncClient

from tests.conftest import auth_header


async def test_unauthenticated_cannot_create_restaurant(client: AsyncClient):
    resp = await client.post(
        "/restaurants/",
        json={"name": "Fast Food", "address": "Ulica 1", "owner_id": 1},
    )
    assert resp.status_code == 401


async def test_list_restaurants_is_public(client: AsyncClient):
    resp = await client.get("/restaurants/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


async def test_customer_cannot_create_restaurant(client: AsyncClient, customer_user):
    headers = await auth_header(client, "testcustomer", "pass123")
    resp = await client.post(
        "/restaurants/",
        json={
            "name": "Illegal Spot",
            "address": "Forbidden St",
            "owner_id": customer_user.id,
        },
        headers=headers,
    )
    assert resp.status_code == 403
    assert resp.json()["code"] == "forbidden"
