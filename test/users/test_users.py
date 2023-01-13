import pytest
from httpx import AsyncClient
from conf_test_db import client

from conf_test_db import app


def test_create_user():
    response = client.post('/auth/register',
                           json={"email": "admin@email.com", "username": "admin", "password": "admin"})
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == "admin@email.com"
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "admin@email.com"
    assert data["id"] == user_id


def test_get_user_v1():
    response = client.get('/users/1/')
    assert response.status_code == 200, response.text
    print(response.json())


@pytest.mark.asyncio
async def test_get_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get('/users/1/')
    assert response.status_code == 200, response.text
