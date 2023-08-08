from fastapi import FastAPI, Path, Body
from fastapi.encoders import jsonable_encoder
from typing import Annotated
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

        collection = db.get_collection("trucks")

        new_truck = collection.insert_one(truck)
        created_truck = collection.find_one({"_id": ObjectId(new_truck.inserted_id)})
        return {"created_truck": created_truck}
    except Exception as e:
        print("An error occurred:", str(e))

@app.patch("/trucks/{truck_id}", response_description="Update a truck", response_model=Truck)
async def update_truck(truck_id: str, truck: UpdateTruckModel = Body(...)):
    truck = {k: v for k, v in truck.dict().items() if v is not None}

    if len(truck) >= 1:

        collection = db.get_collection("trucks")

        update_result = collection.update_one({"_id": ObjectId(truck_id)}, {"$set": truck})

        if update_result.modified_count == 1:
            if (
                updated_truck := collection.find_one({"_id": ObjectId(truck_id)})
            ) is not None:
                return {"updated_truck": updated_truck}

    if (existing_truck := collection.find_one({"_id": ObjectId(truck_id)})) is not None:
        return {"existing_truck": existing_truck}

    return({"status_code": 404, "detail": f"Truck {truck_id} not found"})

@app.delete("/trucks/{truck_id}", response_description="Delete a truck")
async def delete_truck(truck_id: str):
    
    collection = db.get_collection("trucks")
    
    delete_result = collection.delete_one({"_id": ObjectId(truck_id)})
    if delete_result.deleted_count == 1:
        return {"response": "Truck Deleted 204"}

    return({"status_code": 404, "detail": f"Truck {truck_id} not found"})







