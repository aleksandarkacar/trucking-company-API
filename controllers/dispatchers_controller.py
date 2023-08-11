from typing import Annotated
from fastapi import APIRouter, HTTPException, Body, Path
from fastapi.encoders import jsonable_encoder
from models.Dispatcher import Dispatcher, UpdateDispatcherModel
from bson import ObjectId
from utils import serialize_collection
from database_utils import get_truck_drivers_collection

dispatchers_router = APIRouter()
dispatchers = get_truck_drivers_collection()

@dispatchers_router.get("/")
async def get_dispatchers():
    try:
        all_dispatchers = list(dispatchers.find())
        return serialize_collection(all_dispatchers)
    except Exception as e:
        print("An error occurred:", str(e))


@dispatchers_router.get("/{dispatcher_id}")
async def get_dispatcher(
    dispatcher_id: Annotated[str, Path(title= "id of object to get")]
):
    try:
        dispatcher = dispatchers.find_one({"_id": ObjectId(dispatcher_id)})
        return serialize_collection(dispatcher)
    except Exception as e:
        print("An error occurred:", str(e))

@dispatchers_router.post("/", response_description="Add new Dispatcher", response_model=Dispatcher)
async def create_dispatcher(dispatcher: Dispatcher = Body(...)):
    try:
        dispatcher = jsonable_encoder(dispatcher)
        if "_id" in dispatcher:
            del dispatcher["_id"]

        new_dispatcher = dispatchers.insert_one(dispatcher)
        created_dispatcher = dispatchers.find_one({"_id": ObjectId(new_dispatcher.inserted_id)})
        serialized_dispatcher = serialize_collection(created_dispatcher)
        print({"serialized_dispatcher": serialized_dispatcher})
        return serialized_dispatcher
    except Exception as e:
        print("An error occurred:", str(e))

@dispatchers_router.patch("/{dispatcher_id}", response_description="Update a Dispatcher", response_model=Dispatcher)
async def update_dispatcher(dispatcher_id: str, dispatcher_updates: UpdateDispatcherModel = Body(...)):
    dispatcher_updates = {k: v for k, v in dispatcher_updates.dict().items() if v is not None}

    dispatcher = dispatchers.find_one({"_id": ObjectId(dispatcher_id)})
    if dispatcher is None:
        raise HTTPException(status_code=404, detail="Dispatcher not found")
    
    if len(dispatcher_updates) >= 1:
        dispatchers.update_one({"_id": ObjectId(dispatcher_id)}, {"$set": dispatcher_updates})

    if (existing_dispatcher := dispatchers.find_one({"_id": ObjectId(dispatcher_id)})) is not None:
        return serialize_collection(existing_dispatcher)

@dispatchers_router.delete("/{dispatcher_id}", response_description="Delete a Dispatcher")
async def delete_dispatcher(dispatcher_id: str):
    
    delete_result = dispatchers.delete_one({"_id": ObjectId(dispatcher_id)})
    if delete_result.deleted_count == 1:
        return {"response": "Dispatcher Deleted 204"}

    raise HTTPException(status_code=404, detail="Dispatcher not found")