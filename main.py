from fastapi import FastAPI
from models.Truck import Truck
from get_db_pymongo import get_database

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/trucks/")
async def get_trucks():
    try:
        db = get_database()
        collection = db.get_collection("trucks")
        return list(collection.find())
    except Exception as e:
        print("An error occurred:", str(e))
        