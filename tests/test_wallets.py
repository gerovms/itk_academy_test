import pytest

@pytest.mark.asyncio
async def test_wallet_deposit(client, test_user):
    tx_payload = {"operation_type": "DEPOSIT", "amount": 100}
    resp = await client.post(
        f"/api/v1/wallets/{test_user['wallet_id']}/operation",
        json=tx_payload,
        headers=test_user["auth_headers"]
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["amount"] == 100


@pytest.mark.asyncio
async def test_wallet_get(client, test_user):
    resp = await client.get(
        f"/api/v1/wallets/{test_user['wallet_id']}",
        headers=test_user["auth_headers"]
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "amount" in data


@pytest.mark.asyncio
async def test_wallet_not_found(client, test_user):
    resp = await client.get(
        "/api/v1/wallets/999999",
        headers=test_user["auth_headers"]
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Кошелёк не найден"


@pytest.mark.asyncio
async def test_wallet_forbidden(client, test_user, another_user):
    tx_payload = {"operation_type": "DEPOSIT", "amount": 50}
    resp = await client.post(
        f"/api/v1/wallets/{test_user['wallet_id']}/operation",
        json=tx_payload,
        headers=another_user["auth_headers"]
    )
    assert resp.status_code == 403
    assert "Вы не можете управлять чужим кошельком" in resp.json()["detail"]

    resp = await client.get(
        f"/api/v1/wallets/{test_user['wallet_id']}",
        headers=another_user["auth_headers"]
    )
    assert resp.status_code == 403
    assert "Вы не можете иметь доступ к чужому кошельку" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_invalid_transaction_type(client, test_user):
    tx_payload = {"operation_type": "INVALID", "amount": 100}
    resp = await client.post(
        f"/api/v1/wallets/{test_user['wallet_id']}/operation",
        json=tx_payload,
        headers=test_user["auth_headers"]
    )
    assert resp.status_code == 422
    assert any("operation_type" in err["loc"] for err in resp.json()["detail"])
