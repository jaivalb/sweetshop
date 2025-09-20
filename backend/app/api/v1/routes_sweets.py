from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument

from app.api.v1.deps import get_current_user, get_current_admin
from app.db.mongo import get_db
from app.models.sweet import SweetCreate, SweetUpdate
from app.utils.mongo import to_object_id, doc_to_public

router = APIRouter(prefix="/api/sweets", tags=["sweets"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_sweet(sweet: SweetCreate, db: AsyncIOMotorDatabase = Depends(get_db), user = Depends(get_current_admin)):
	doc = sweet.model_dump()
	res = await db["sweets"].insert_one(doc)
	created = await db["sweets"].find_one({"_id": res.inserted_id})
	return doc_to_public(created)


@router.get("/")
@router.get("")
async def list_sweets(db: AsyncIOMotorDatabase = Depends(get_db), user = Depends(get_current_user)):
	cursor = db["sweets"].find({})
	return [doc_to_public(d) async for d in cursor]


@router.get("/search")
async def search_sweets(q: str | None = None, category: str | None = None, min_price: float | None = None, max_price: float | None = None, db: AsyncIOMotorDatabase = Depends(get_db), user = Depends(get_current_user)):
	filters = {}
	if q:
		filters["name"] = {"$regex": q, "$options": "i"}
	if category:
		filters["category"] = category
	price = {}
	if min_price is not None:
		price["$gte"] = float(min_price)
	if max_price is not None:
		price["$lte"] = float(max_price)
	if price:
		filters["price"] = price
	cursor = db["sweets"].find(filters)
	return [doc_to_public(d) async for d in cursor]


@router.put("/{sweet_id}")
async def update_sweet(sweet_id: str, update: SweetUpdate, db: AsyncIOMotorDatabase = Depends(get_db), user = Depends(get_current_admin)):
	changes = {k: v for k, v in update.model_dump(exclude_none=True).items()}
	found = await db["sweets"].find_one_and_update(
		{"_id": to_object_id(sweet_id)},
		{"$set": changes},
		return_document=ReturnDocument.AFTER,
	)
	if not found:
		raise HTTPException(status_code=404, detail="Sweet not found")
	return doc_to_public(found)


@router.delete("/{sweet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sweet(sweet_id: str, db: AsyncIOMotorDatabase = Depends(get_db), user = Depends(get_current_admin)):
	await db["sweets"].delete_one({"_id": to_object_id(sweet_id)})
	return


@router.post("/{sweet_id}/purchase")
async def purchase_sweet(sweet_id: str, quantity: int = 1, db: AsyncIOMotorDatabase = Depends(get_db), user = Depends(get_current_user)):
	if quantity <= 0:
		raise HTTPException(status_code=400, detail="Quantity must be positive")
	res = await db["sweets"].find_one_and_update(
		{"_id": to_object_id(sweet_id), "quantity": {"$gte": quantity}},
		{"$inc": {"quantity": -quantity}},
		return_document=ReturnDocument.AFTER,
	)
	if not res:
		raise HTTPException(status_code=400, detail="Insufficient stock or not found")
	return doc_to_public(res)


@router.post("/{sweet_id}/restock")
async def restock_sweet(sweet_id: str, quantity: int = 1, db: AsyncIOMotorDatabase = Depends(get_db), user = Depends(get_current_admin)):
	if quantity <= 0:
		raise HTTPException(status_code=400, detail="Quantity must be positive")
	res = await db["sweets"].find_one_and_update(
		{"_id": to_object_id(sweet_id)},
		{"$inc": {"quantity": quantity}},
		return_document=ReturnDocument.AFTER,
	)
	if not res:
		raise HTTPException(status_code=404, detail="Sweet not found")
	return doc_to_public(res)
