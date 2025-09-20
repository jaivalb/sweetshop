from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserInDB(BaseModel):
	id: Optional[str] = Field(default=None, alias="_id")
	email: EmailStr
	full_name: Optional[str] = None
	hashed_password: str
	is_admin: bool = False

	class Config:
		populate_by_name = True


class UserCreate(BaseModel):
	email: EmailStr
	full_name: Optional[str] = None
	password: str
	is_admin: bool = False


class UserPublic(BaseModel):
	id: str
	email: EmailStr
	full_name: Optional[str] = None
	is_admin: bool = False


class Token(BaseModel):
	access_token: str
	token_type: str = "bearer"
