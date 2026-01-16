import pytest

@pytest.mark.asyncio
async def test_login_success(client):
    response = await client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
