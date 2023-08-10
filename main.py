from fastapi import FastAPI
from database_utils import get_trucks_collection, get_managers_collection, get_dispatchers_collection, get_trailers_collection, get_truck_drivers_collection
from controllers.trucks_controller import trucks_router
from controllers.trailers_controller import trailers_router
from controllers.truck_drivers_controller import truck_drivers_router
from controllers.managers_controller import managers_router
from controllers.dispatchers_controller import dispatchers_router

app = FastAPI()

trucks = get_trucks_collection()
trailers = get_trailers_collection()
managers = get_managers_collection()
dispatchers = get_dispatchers_collection()
truck_drivers = get_truck_drivers_collection()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(trucks_router, prefix="/trucks", tags=["trucks"])
app.include_router(trailers_router, prefix="/trailers", tags=["trailers"])
app.include_router(truck_drivers_router, prefix="/truck_drivers", tags=["truck_drivers"])
app.include_router(managers_router, prefix="/managers", tags=["managers"])
app.include_router(dispatchers_router, prefix="/dispatchers", tags=["dispatchers"])

#TODO Finish PUT paths for manager and dispatcher, and fix what props are optional for truck driver and dispatcher



