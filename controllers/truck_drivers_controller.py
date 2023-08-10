from typing import Annotated
from fastapi import APIRouter, HTTPException, Body, Path
from fastapi.encoders import jsonable_encoder
from models.TruckDriver import TruckDriver, UpdateTruckDriverModel
from bson import ObjectId
from utils import serialize_collection
from database_utils import get_truck_drivers_collection

truck_drivers_router = APIRouter()
truck_drivers = get_truck_drivers_collection()

@truck_drivers_router.get("/")
async def get_truck_drivers():
    try:
        all_truck_drivers = list(truck_drivers.find())
        return serialize_collection(all_truck_drivers)
    except Exception as e:
        print("An error occurred:", str(e))


@truck_drivers_router.get("/{truck_driver_id}")
async def get_truck_driver(
    truck_driver_id: Annotated[str, Path(title= "id of object to get")]
):
    try:
        truck_driver = truck_drivers.find_one({"_id": ObjectId(truck_driver_id)})
        return serialize_collection(truck_driver)
    except Exception as e:
        print("An error occurred:", str(e))

@truck_drivers_router.post("/", response_description="Add new Truck driver", response_model=TruckDriver)
async def create_truck_driver(truck_driver: TruckDriver = Body(...)):
    try:
        truck_driver = jsonable_encoder(truck_driver)
        if "_id" in truck_driver:
            del truck_driver["_id"]

        new_truck_driver = truck_drivers.insert_one(truck_driver)
        created_truck_driver = truck_drivers.find_one({"_id": ObjectId(new_truck_driver.inserted_id)})
        return serialize_collection(created_truck_driver)
    except Exception as e:
        print("An error occurred:", str(e))

@truck_drivers_router.patch("/{truck_driver_id}", response_description="Update a Truck driver", response_model=TruckDriver)
async def update_truck_driver(truck_driver_id: str, truck_driver_updates: UpdateTruckDriverModel = Body(...)):
    truck_driver_updates = {k: v for k, v in truck_driver_updates.dict().items() if v is not None}

    truck_driver = truck_drivers.find_one({"_id": ObjectId(truck_driver_id)})
    if truck_driver is None:
        raise HTTPException(status_code=404, detail="Truck driver not found")
    
    if len(truck_driver_updates) >= 1:
        truck_drivers.update_one({"_id": ObjectId(truck_driver_id)}, {"$set": truck_driver_updates})

    if (existing_truck_driver := truck_drivers.find_one({"_id": ObjectId(truck_driver_id)})) is not None:
        return serialize_collection(existing_truck_driver)

@truck_drivers_router.delete("/{truck_driver_id}", response_description="Delete a truck driver")
async def delete_truck_driver(truck_driver_id: str):
    
    delete_result = truck_drivers.delete_one({"_id": ObjectId(truck_driver_id)})
    if delete_result.deleted_count == 1:
        return {"response": "Truck driver Deleted 204"}

    raise HTTPException(status_code=404, detail="Truck driver not found")