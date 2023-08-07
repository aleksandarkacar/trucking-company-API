from fastapi import FastAPI
from models.Truck import Truck

app = FastAPI()
    

@app.get("/")
async def root():
    return {"message": "Hello World"}