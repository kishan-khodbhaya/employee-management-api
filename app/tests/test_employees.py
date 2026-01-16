import pytest

@pytest.mark.asyncio
async def test_get_employees_unauthorized(client):
    response = await client.get("/employees/")
    assert response.status_code == 401
