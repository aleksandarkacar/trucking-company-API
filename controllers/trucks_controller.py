from typing import Annotated
from fastapi import APIRouter, HTTPException, Body, Path
from fastapi.encoders import jsonable_encoder
from models.Truck import Truck, UpdateTruckModel
from models.Repair import RepairModel
from bson import ObjectId
from utils import serialize_collection
from database_utils import get_trucks_collection

trucks_router = APIRouter()
trucks = get_trucks_collection()

@trucks_router.get("/")
async def get_trucks():
    try:
        all_trucks = list(trucks.find())
        return serialize_collection(all_trucks)
    except Exception as e:
        print("An error occurred:", str(e))

@trucks_router.get("/{truck_id}")
async def get_truck(
    truck_id: Annotated[str, Path(title= "id of object to get")]
):
    try:
        single_truck = trucks.find_one({"_id": ObjectId(truck_id)})
        return serialize_collection(single_truck)
    except Exception as e:
        print("An error occurred:", str(e))

@trucks_router.post("/", response_description="Add new truck", response_model=Truck)
async def create_truck(truck: Truck = Body(...)):
    try:
        truck = jsonable_encoder(truck)
        if "_id" in truck:
            del truck["_id"]
        new_truck = trucks.insert_one(truck)
        created_truck = trucks.find_one({"_id": ObjectId(new_truck.inserted_id)})
        return serialize_collection(created_truck)
    except Exception as e:
        print("An error occurred:", str(e))

@trucks_router.patch("/{truck_id}", response_description="Update a truck", response_model=Truck)
async def update_truck(truck_id: str, truck_updates: UpdateTruckModel = Body(...)):
    truck_updates = {k: v for k, v in truck_updates.dict().items() if v is not None}

    truck = trucks.find_one({"_id": ObjectId(truck_id)})
    if truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")
    
    if len(truck_updates) >= 1:
        trucks.update_one({"_id": ObjectId(truck_id)}, {"$set": truck_updates})

    if (existing_truck := trucks.find_one({"_id": ObjectId(truck_id)})) is not None:
        return serialize_collection(existing_truck)

@trucks_router.put("/{truck_id}/add_repair", response_model=Truck)
async def update_repairs(truck_id: str, repair: RepairModel = Body(...)):

    truck = trucks.find_one({"_id": ObjectId(truck_id)})
    if truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")

    repair_history_list = truck.get("repair_history_list", [])
    repair_history_list.append(repair.model_dump())
    
    update_result = trucks.update_one(
        {"_id": ObjectId(truck_id)},
        {"$set": {"repair_history_list": repair_history_list}}
    )
    if update_result.modified_count == 1:
        if (existing_truck := trucks.find_one({"_id": ObjectId(truck_id)})) is not None:
            return serialize_collection(existing_truck)
    
    raise HTTPException(status_code=500, detail="Failed to update repairs")

@trucks_router.delete("/{truck_id}", response_description="Delete a truck")
async def delete_truck(truck_id: str):
    
    delete_result = trucks.delete_one({"_id": ObjectId(truck_id)})
    if delete_result.deleted_count == 1:
        return {"response": "Truck Deleted 204"}

    raise HTTPException(status_code=404, detail="Truck not found")