from fastapi import FastAPI, Path
from typing import Annotated
from models.Truck import Truck
from get_db_pymongo import get_database
from bson import ObjectId
from utils import serialize_collection

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/trucks/")
async def get_trucks():
    try:
        db = get_database()
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
        db = get_database()
        collection = db.get_collection("trucks")
        trucks = collection.find_one({"_id": ObjectId(truck_id)})
        
        return {"serialized_trucks": serialize_collection(trucks)}
    except Exception as e:
        print("An error occurred:", str(e))


