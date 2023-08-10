from typing import Annotated
from fastapi import APIRouter, HTTPException, Body, Path
from fastapi.encoders import jsonable_encoder
from models.Trailer import Trailer, UpdateTrailerModel
from models.Repair import RepairModel
from bson import ObjectId
from utils import serialize_collection
from database_utils import get_trailers_collection

trailers_router = APIRouter()
trailers = get_trailers_collection()

@trailers_router.get("/")
async def get_trailers():
    try:
        all_trailers = list(trailers.find())
        return serialize_collection(all_trailers)
    except Exception as e:
        print("An error occurred:", str(e))


@trailers_router.get("/{trailer_id}")
async def get_trailer(
    trailer_id: Annotated[str, Path(title= "id of object to get")]
):
    try:
        trailer = trailers.find_one({"_id": ObjectId(trailer_id)})
        return serialize_collection(trailer)
    except Exception as e:
        print("An error occurred:", str(e))

@trailers_router.post("/", response_description="Add new trailer", response_model=Trailer)
async def create_trailer(trailer: Trailer = Body(...)):
    try:
        trailer = jsonable_encoder(trailer)
        if "_id" in trailer:
            del trailer["_id"]

        new_trailer = trailers.insert_one(trailer)
        created_trailer = trailers.find_one({"_id": ObjectId(new_trailer.inserted_id)})
        serialized_trailer = serialize_collection(created_trailer)
        return serialized_trailer
    except Exception as e:
        print("An error occurred:", str(e))

@trailers_router.patch("/{trailer_id}", response_description="Update a trailer", response_model=Trailer)
async def update_trailer(trailer_id: str, trailer_updates: UpdateTrailerModel = Body(...)):
    trailer_updates = {k: v for k, v in trailer_updates.dict().items() if v is not None}
    trailer = trailers.find_one({"_id": ObjectId(trailer_id)})
    if trailer is None:
        raise HTTPException(status_code=404, detail="Trailer not found")
    
    if len(trailer_updates) >= 1:
        trailers.update_one({"_id": ObjectId(trailer_id)}, {"$set": trailer_updates})

    if (existing_trailer := trailers.find_one({"_id": ObjectId(trailer_id)})) is not None:
        return serialize_collection(existing_trailer)
    
@trailers_router.put("/{trailer_id}/add_repair", response_model=Trailer)
async def update_repairs(trailer_id: str, repair: RepairModel = Body(...)):
    repair = jsonable_encoder(repair)
    if "_id" in repair:
        del repair["_id"]
    trailer = trailers.find_one({"_id": ObjectId(trailer_id)})
    if trailer is None:
        raise HTTPException(status_code=404, detail="Trailer not found")

    repair_history_list = trailer.get("repair_history_list", [])
    repair_history_list.append(repair.dict())
    
    update_result = trailers.update_one(
        {"_id": ObjectId(trailer_id)},
        {"$set": {"repair_history_list": repair_history_list}}
    )
    if update_result.modified_count == 1:
        if (existing_trailer := trailers.find_one({"_id": ObjectId(trailer_id)})) is not None:
            return serialize_collection(existing_trailer)
    
    raise HTTPException(status_code=500, detail="Failed to update repairs")

@trailers_router.delete("/{trailer_id}", response_description="Delete a trailer")
async def delete_trailer(trailer_id: str):
    delete_result = trailers.delete_one({"_id": ObjectId(trailer_id)})
    if delete_result.deleted_count == 1:
        return {"response": "trailer Deleted 204"}
    raise HTTPException(status_code=404, detail="Trailer not found")
