from typing import Annotated
from fastapi import APIRouter, HTTPException, Body, Path
from fastapi.encoders import jsonable_encoder
from models.Manager import Manager, UpdateManagerModel
from bson import ObjectId
from utils import serialize_collection
from database_utils import get_truck_drivers_collection

managers_router = APIRouter()
managers = get_truck_drivers_collection()

@managers_router.get("/")
async def get_managers():
    try:
        all_managers = list(managers.find())
        return serialize_collection(all_managers)
    except Exception as e:
        print("An error occurred:", str(e))


@managers_router.get("/{manager_id}")
async def get_manager(
    manager_id: Annotated[str, Path(title= "id of object to get")]
):
    try:
        manager = managers.find_one({"_id": ObjectId(manager_id)})
        return serialize_collection(manager)
    except Exception as e:
        print("An error occurred:", str(e))

@managers_router.post("/", response_description="Add new manager", response_model=Manager)
async def create_manager(manager: Manager = Body(...)):
    try:
        manager = jsonable_encoder(manager)
        if "_id" in manager:
            del manager["_id"]

        new_manager = managers.insert_one(manager)
        created_manager = managers.find_one({"_id": ObjectId(new_manager.inserted_id)})
        serialized_manager = serialize_collection(created_manager)
        print({"serialized_manager": serialized_manager})
        return serialized_manager
    except Exception as e:
        print("An error occurred:", str(e))

@managers_router.patch("/{manager_id}", response_description="Update a manager", response_model=Manager)
async def update_manager(manager_id: str, manager_updates: UpdateManagerModel = Body(...)):
    manager_updates = {k: v for k, v in manager_updates.dict().items() if v is not None}

    manager = managers.find_one({"_id": ObjectId(manager_id)})
    if manager is None:
        raise HTTPException(status_code=404, detail="Manager not found")
    
    if len(manager_updates) >= 1:
        managers.update_one({"_id": ObjectId(manager_id)}, {"$set": manager_updates})

    if (existing_manager := managers.find_one({"_id": ObjectId(manager_id)})) is not None:
        return serialize_collection(existing_manager)

@managers_router.delete("/{manager_id}", response_description="Delete a manager")
async def delete_manager(manager_id: str):
    
    delete_result = managers.delete_one({"_id": ObjectId(manager_id)})
    if delete_result.deleted_count == 1:
        return {"response": "Manager Deleted 204"}

    return({"status_code": 404, "detail": f"Manager {manager_id} not found"})