from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.security import create_access_token, hash_password, verify_password
from app.db.mongo import get_db
from app.models.user import UserCreate, Token, UserPublic
from app.models.auth import LoginRequest
from app.api.v1.deps import get_current_user
from app.utils.mongo import doc_to_public

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
	existing = await db["users"].find_one({"email": user_in.email})
	if existing:
		raise HTTPException(status_code=400, detail="Email already registered")
	user_doc = {
		"email": user_in.email,
		"full_name": user_in.full_name,
		"hashed_password": hash_password(user_in.password),
		"is_admin": bool(user_in.is_admin),
	}
	res = await db["users"].insert_one(user_doc)
	token = create_access_token(subject=user_in.email)
	return Token(access_token=token)


@router.post("/login", response_model=Token)
async def login(user_in: LoginRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
	user = await db["users"].find_one({"email": user_in.email})
	if not user or not verify_password(user_in.password, user["hashed_password"]):
		raise HTTPException(status_code=400, detail="Invalid credentials")
	token = create_access_token(subject=user_in.email)
	return Token(access_token=token)


@router.get("/me", response_model=UserPublic)
async def me(user = Depends(get_current_user)):
    return doc_to_public(user)
