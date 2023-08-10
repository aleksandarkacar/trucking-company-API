from typing import Annotated
from controllers.controller_helpers.trailers_helpers import create_trailer_helper, update_repair_helper, update_trailer_helper
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
        return create_trailer_helper(trailer, trailers)
    except Exception as e:
        print("An error occurred:", str(e))

@trailers_router.patch("/{trailer_id}", response_description="Update a trailer", response_model=Trailer)
async def update_trailer(trailer_id: str, trailer_updates: UpdateTrailerModel = Body(...)):
    return update_trailer_helper(trailer_id, trailer_updates, trailers)
    
@trailers_router.put("/{trailer_id}/add_repair", response_model=Trailer)
async def update_repairs(trailer_id: str, repair: RepairModel = Body(...)):
    return update_repair_helper(trailer_id, repair, trailers)

@trailers_router.delete("/{trailer_id}", response_description="Delete a trailer")
async def delete_trailer(trailer_id: str):
    delete_result = trailers.delete_one({"_id": ObjectId(trailer_id)})
    if delete_result.deleted_count == 1:
        return {"response": "trailer Deleted 204"}
    raise HTTPException(status_code=404, detail="Trailer not found")
