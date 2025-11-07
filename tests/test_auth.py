import pytest

@pytest.mark.asyncio
async def test_register_user(client):
    payload = {"username": "newuser", "password": "123456"}
    resp = await client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "id" in data
    assert data["username"] == "newuser"


@pytest.mark.asyncio
async def test_login_user(client, test_user):
    resp = await client.post(
        "/api/v1/auth/login",
        json={
            "username": test_user["username"],
            "password": test_user["password"]
            }
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
