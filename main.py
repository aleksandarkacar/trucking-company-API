from fastapi import FastAPI, HTTPException, Path, Body
from fastapi.encoders import jsonable_encoder
from typing import Annotated
from models.Repair import RepairModel
from models.Truck import Truck, UpdateTruckModel
from get_db_pymongo import get_database
from bson import ObjectId
from utils import serialize_collection

app = FastAPI()

db = get_database()
collection = db.get_collection("trucks")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/trucks/")
async def get_trucks():
    try:
        trucks = list(collection.find())
        
        return {"serialized_trucks": serialize_collection(trucks)}
    except Exception as e:
        print("An error occurred:", str(e))

@app.get("/trucks/{truck_id}")
async def get_truck(
    truck_id: Annotated[str, Path(title= "id of object to get")]
):
    try:
        collection = db.get_collection("trucks")
        truck = collection.find_one({"_id": ObjectId(truck_id)})
        
        return {"serialized_truck": serialize_collection(truck)}
    except Exception as e:
        print("An error occurred:", str(e))

@app.post("/trucks/", response_description="Add new truck", response_model=Truck)
async def create_truck(truck: Truck = Body(...)):
    try:
        truck = jsonable_encoder(truck)
        if "_id" in truck:
            del truck["_id"] #{_id: None} was registering as a duplicate id

        collection = db.get_collection("trucks")

        new_truck = collection.insert_one(truck)
        created_truck = collection.find_one({"_id": ObjectId(new_truck.inserted_id)})
        serialized_truck = serialize_collection(created_truck)
        print({"serialized_truck": serialized_truck})
        return serialized_truck
    except Exception as e:
        print("An error occurred:", str(e))

@app.patch("/trucks/{truck_id}", response_description="Update a truck", response_model=Truck)
async def update_truck(truck_id: str, truck_updates: UpdateTruckModel = Body(...)):
    truck_updates = {k: v for k, v in truck_updates.dict().items() if v is not None}

    collection = db.get_collection("trucks")

    truck = collection.find_one({"_id": ObjectId(truck_id)})
    if truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")
    
    if len(truck_updates) >= 1:
        collection.update_one({"_id": ObjectId(truck_id)}, {"$set": truck_updates})

    if (existing_truck := collection.find_one({"_id": ObjectId(truck_id)})) is not None:
        return serialize_collection(existing_truck)

@app.put("/trucks/{truck_id}/add_repair", response_model=Truck)
async def update_repairs(truck_id: str, repair: RepairModel = Body(...)):

    collection = db.get_collection("trucks")

    truck = collection.find_one({"_id": ObjectId(truck_id)})
    if truck is None:
        raise HTTPException(status_code=404, detail="Truck not found")

    repair_history_list = truck.get("repair_history_list", [])
    repair_history_list.append(repair.dict())
    
    update_result = collection.update_one(
        {"_id": ObjectId(truck_id)},
        {"$set": {"repair_history_list": repair_history_list}}
    )
    if update_result.modified_count == 1:
        if (existing_truck := collection.find_one({"_id": ObjectId(truck_id)})) is not None:
            return serialize_collection(existing_truck)
    
    raise HTTPException(status_code=500, detail="Failed to update repairs")

@app.delete("/trucks/{truck_id}", response_description="Delete a truck")
async def delete_truck(truck_id: str):
    
    collection = db.get_collection("trucks")
    
    delete_result = collection.delete_one({"_id": ObjectId(truck_id)})
    if delete_result.deleted_count == 1:
        return {"response": "Truck Deleted 204"}

    return({"status_code": 404, "detail": f"Truck {truck_id} not found"})







