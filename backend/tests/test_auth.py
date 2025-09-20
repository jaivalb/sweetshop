import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_and_login(test_client: AsyncClient):
	# register
	resp = await test_client.post("/api/auth/register", json={
		"email": "user@example.com",
		"full_name": "Test User",
		"password": "secret123",
		"is_admin": False
	})
	assert resp.status_code == 201
	data = resp.json()
	assert "access_token" in data

	# login
	resp2 = await test_client.post("/api/auth/login", json={
		"email": "user@example.com",
		"password": "secret123"
	})
	assert resp2.status_code == 200
	data2 = resp2.json()
	assert "access_token" in data2
