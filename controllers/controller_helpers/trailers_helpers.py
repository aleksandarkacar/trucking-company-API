from bson import ObjectId
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from utils import serialize_collection        

def create_trailer_helper(trailer, trailers):
    trailer = jsonable_encoder(trailer)
    if "_id" in trailer:
        del trailer["_id"]

    new_trailer = trailers.insert_one(trailer)
    created_trailer = trailers.find_one({"_id": new_trailer.inserted_id})
    return serialize_collection(created_trailer)

def update_trailer_helper(trailer_id, trailer_updates, trailers):
    trailer_updates = {k: v for k, v in trailer_updates.model_dump().items() if v is not None}
    trailer = trailers.find_one({"_id": ObjectId(trailer_id)})
    if trailer is None:
        raise HTTPException(status_code=404, detail="Trailer not found")
    
    if len(trailer_updates) >= 1:
        trailers.update_one({"_id": ObjectId(trailer_id)}, {"$set": trailer_updates})

    if (existing_trailer := trailers.find_one({"_id": ObjectId(trailer_id)})) is not None:
        return serialize_collection(existing_trailer)
    
def update_repair_helper(trailer_id, repair, trailers):
    repair = jsonable_encoder(repair)
    if "_id" in repair:
        repair["_id"] = str(ObjectId())
    trailer = trailers.find_one({"_id": ObjectId(trailer_id)})
    if trailer is None:
        raise HTTPException(status_code=404, detail="Trailer not found")

    repair_history_list = trailer.get("repair_history_list", [])
    repair_history_list.append(repair)
    
    update_result = trailers.update_one(
        {"_id": ObjectId(trailer_id)},
        {"$set": {"repair_history_list": repair_history_list}}
    )
    if update_result.modified_count == 1:
        if (existing_trailer := trailers.find_one({"_id": ObjectId(trailer_id)})) is not None:
            return serialize_collection(existing_trailer)
    
    raise HTTPException(status_code=500, detail="Failed to update repairs")