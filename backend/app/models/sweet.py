from typing import Optional
from pydantic import BaseModel, Field


class SweetInDB(BaseModel):
	id: Optional[str] = Field(default=None, alias="_id")
	name: str
	category: str
	price: float
	quantity: int

	class Config:
		populate_by_name = True


class SweetCreate(BaseModel):
	name: str
	category: str
	price: float
	quantity: int = 0


class SweetUpdate(BaseModel):
	name: Optional[str] = None
	category: Optional[str] = None
	price: Optional[float] = None
	quantity: Optional[int] = None


class SweetPublic(BaseModel):
	id: str
	name: str
	category: str
	price: float
	quantity: int
