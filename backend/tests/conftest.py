import asyncio
import os
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from pymongo.errors import PyMongoError

os.environ.setdefault("MONGO_URI", "mongodb://root:example@localhost:27017")
os.environ.setdefault("MONGO_DB", "sweetshop_test")

from app.main import app  # noqa: E402
from app.db.mongo import get_database, get_client  # noqa: E402


@pytest.fixture(scope="session")
def event_loop():
	loop = asyncio.get_event_loop_policy().new_event_loop()
	yield loop
	loop.close()


@pytest.fixture(autouse=True, scope="session")
async def _db_setup_teardown():
	client = get_client()
	yield
	try:
		await client.drop_database(os.environ.get("MONGO_DB", "sweetshop_test"))
	except Exception:
		pass


@pytest.fixture
async def test_client() -> AsyncClient:
	async with LifespanManager(app):
		async with AsyncClient(app=app, base_url="http://test") as ac:
			yield ac
