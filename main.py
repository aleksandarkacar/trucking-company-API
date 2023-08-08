from fastapi import FastAPI, Path, Body
from fastapi.encoders import jsonable_encoder
from typing import Annotated
from models.Truck import Truck
from get_db_pymongo import get_database
from bson import ObjectId
from utils import serialize_collection

app = FastAPI()

db = get_database()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/trucks/")
async def get_trucks():
    try:
        collection = db.get_collection("trucks")
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



