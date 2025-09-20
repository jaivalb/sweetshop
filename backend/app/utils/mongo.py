from typing import Any, Dict, Optional

from bson import ObjectId


def to_object_id(id_str: str) -> ObjectId:
	return ObjectId(id_str)


def doc_to_public(doc: Dict[str, Any]) -> Dict[str, Any]:
	out = dict(doc)
	_id = out.pop("_id", None)
	# remove sensitive fields if present
	if "hashed_password" in out:
		out.pop("hashed_password", None)
	if isinstance(_id, ObjectId):
		out["id"] = str(_id)
	elif _id is not None and "id" not in out:
		out["id"] = str(_id)
	return out
