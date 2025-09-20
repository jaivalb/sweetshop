from typing import AsyncGenerator
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

_client: AsyncIOMotorClient | None = None


def _ensure_auth_source(uri: str) -> str:
	parsed = urlparse(uri)
	# Only modify when credentials are present and authSource missing
	if parsed.username:
		qs = parse_qs(parsed.query, keep_blank_values=True)
		if "authSource" not in qs:
			qs["authSource"] = ["admin"]
			new_query = urlencode(qs, doseq=True)
			return urlunparse(parsed._replace(query=new_query))
	return uri


def _sanitize_uri(uri: str) -> str:
	parsed = urlparse(uri)
	netloc = parsed.hostname or "localhost"
	if parsed.port:
		netloc += f":{parsed.port}"
	# Rebuild without credentials
	return urlunparse((parsed.scheme, netloc, parsed.path or "/", "", parsed.query, ""))


def get_client() -> AsyncIOMotorClient:
	global _client
	if _client is None:
		uri = _ensure_auth_source(settings.mongo_uri)
		_client = AsyncIOMotorClient(uri)
	return _client


def get_database() -> AsyncIOMotorDatabase:
	return get_client()[settings.database_name]


async def lifespan(app):
	client = get_client()
	try:
		await client.admin.command("ping")
		parsed = urlparse(_ensure_auth_source(settings.mongo_uri))
		auth_source = parse_qs(parsed.query).get("authSource", [None])[0]
		logging.getLogger("uvicorn").info(
			f"Mongo connected: uri={_sanitize_uri(parsed.geturl())} user={'set' if parsed.username else 'none'} authSource={auth_source} db={settings.database_name}"
		)
        # Ensure indexes
        db = get_database()
        await db["users"].create_index("email", unique=True)
        await db["sweets"].create_index([("name", 1)])
	except Exception as exc:
		logging.getLogger("uvicorn").error(f"Mongo connection failed: {exc}")
	yield
	client.close()


async def get_db() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
	yield get_database()
