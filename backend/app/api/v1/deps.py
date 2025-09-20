from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import settings
from app.db.mongo import get_db

security = HTTPBearer()


async def get_current_user(
	db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
	token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
	try:
		payload = jwt.decode(token.credentials, settings.secret_key, algorithms=["HS256"])
		sub: Optional[str] = payload.get("sub")
		if sub is None:
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
		user = await db["users"].find_one({"email": sub})
		if not user:
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
		return user
	except JWTError:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


async def get_current_admin(user = Depends(get_current_user)):
	if not user.get("is_admin", False):
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
	return user
