import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_sweets_admin_and_user_flows(test_client: AsyncClient):
	# create admin
	admin_reg = await test_client.post("/api/auth/register", json={
		"email": "admin@example.com",
		"full_name": "Admin",
		"password": "secret123",
		"is_admin": True
	})
	assert admin_reg.status_code == 201
	admin_token = admin_reg.json()["access_token"]

	# admin adds sweet
	resp_add = await test_client.post("/api/sweets/", json={
		"name": "Lollipop",
		"category": "Candy",
		"price": 1.5,
		"quantity": 10
	}, headers={"Authorization": f"Bearer {admin_token}"})
	assert resp_add.status_code == 201
	created = resp_add.json()
	assert created["name"] == "Lollipop"
	sweet_id = created["id"]

	# normal user registers
	user_reg = await test_client.post("/api/auth/register", json={
		"email": "user2@example.com",
		"full_name": "User Two",
		"password": "secret123",
		"is_admin": False
	})
	assert user_reg.status_code == 201
	user_token = user_reg.json()["access_token"]

	# list sweets
	resp_list = await test_client.get("/api/sweets/", headers={"Authorization": f"Bearer {user_token}"})
	assert resp_list.status_code == 200
	items = resp_list.json()
	assert any(i["name"] == "Lollipop" for i in items)

	# search sweets
	resp_search = await test_client.get("/api/sweets/search", params={"q": "lolli"}, headers={"Authorization": f"Bearer {user_token}"})
	assert resp_search.status_code == 200
	search_items = resp_search.json()
	assert any(i["name"] == "Lollipop" for i in search_items)

	# purchase
	resp_purchase = await test_client.post(f"/api/sweets/{sweet_id}/purchase", params={"quantity": 2}, headers={"Authorization": f"Bearer {user_token}"})
	assert resp_purchase.status_code == 200
	purchased = resp_purchase.json()
	assert purchased["quantity"] == 8

	# restock by admin
	resp_restock = await test_client.post(
		f"/api/sweets/{sweet_id}/restock",
		params={"quantity": 5},
		headers={"Authorization": f"Bearer {admin_token}"}
	)
	assert resp_restock.status_code == 200
	restocked = resp_restock.json()
	assert restocked["quantity"] == 13

	# update by admin
	resp_update = await test_client.put(
		f"/api/sweets/{sweet_id}",
		json={"price": 2.0},
		headers={"Authorization": f"Bearer {admin_token}"}
	)
	assert resp_update.status_code == 200
	updated = resp_update.json()
	assert updated["price"] == 2.0

	# delete by admin
	resp_delete = await test_client.delete(f"/api/sweets/{sweet_id}", headers={"Authorization": f"Bearer {admin_token}"})
	assert resp_delete.status_code == 204

	# ensure not found
	resp_list2 = await test_client.get("/api/sweets/", headers={"Authorization": f"Bearer {user_token}"})
	assert all(i["id"] != sweet_id for i in resp_list2.json())
