from fastapi import FastAPI, HTTPException, Path, Body
from fastapi.encoders import jsonable_encoder
from typing import Annotated
from models.Dispatcher import Dispatcher, UpdateDispatcherModel
from models.Repair import RepairModel
from models.Trailer import Trailer, UpdateTrailerModel
from models.Truck import Truck, UpdateTruckModel
from models.Manager import Manager, UpdateManagerModel
from get_db_pymongo import get_database
from bson import ObjectId
from models.TruckDriver import TruckDriver, UpdateTruckDriverModel
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
        if "_id" in truck:
            del truck["_id"]

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


#Trailer API paths

@app.get("/trailers/")
async def get_trailers():
    try:
        collection = db.get_collection("trailers")
        trailers = list(collection.find())
        
        return {"serialized_trailers": serialize_collection(trailers)}
    except Exception as e:
        print("An error occurred:", str(e))


@app.get("/trailers/{trailer_id}")
async def get_trailer(
    trailer_id: Annotated[str, Path(title= "id of object to get")]
):
    try:
        collection = db.get_collection("trailers")
        trailer = collection.find_one({"_id": ObjectId(trailer_id)})
        
        return {"serialized_trailer": serialize_collection(trailer)}
    except Exception as e:
        print("An error occurred:", str(e))

@app.post("/trailers/", response_description="Add new trailer", response_model=Trailer)
async def create_trailer(trailer: Trailer = Body(...)):
    try:
        trailer = jsonable_encoder(trailer)
        if "_id" in trailer:
            del trailer["_id"]

        collection = db.get_collection("trailers")

        new_trailer = collection.insert_one(trailer)
        created_trailer = collection.find_one({"_id": ObjectId(new_trailer.inserted_id)})
        serialized_trailer = serialize_collection(created_trailer)
        print({"serialized_trailer": serialized_trailer})
        return serialized_trailer
    except Exception as e:
        print("An error occurred:", str(e))

@app.patch("/trailers/{trailer_id}", response_description="Update a trailer", response_model=Trailer)
async def update_trailer(trailer_id: str, trailer_updates: UpdateTrailerModel = Body(...)):
    trailer_updates = {k: v for k, v in trailer_updates.dict().items() if v is not None}

    collection = db.get_collection("trailers")
    trailer = collection.find_one({"_id": ObjectId(trailer_id)})
    if trailer is None:
        raise HTTPException(status_code=404, detail="Trailer not found")
    
    if len(trailer_updates) >= 1:
        collection.update_one({"_id": ObjectId(trailer_id)}, {"$set": trailer_updates})

    if (existing_trailer := collection.find_one({"_id": ObjectId(trailer_id)})) is not None:
        return serialize_collection(existing_trailer)
    
@app.put("/trailers/{trailer_id}/add_repair", response_model=Trailer)
async def update_repairs(trailer_id: str, repair: RepairModel = Body(...)):

    collection = db.get_collection("trailers")

    trailer = collection.find_one({"_id": ObjectId(trailer_id)})
    if trailer is None:
        raise HTTPException(status_code=404, detail="Trailer not found")

    repair_history_list = trailer.get("repair_history_list", [])
    repair_history_list.append(repair.dict())
    
    update_result = collection.update_one(
        {"_id": ObjectId(trailer_id)},
        {"$set": {"repair_history_list": repair_history_list}}
    )
    if update_result.modified_count == 1:
        if (existing_trailer := collection.find_one({"_id": ObjectId(trailer_id)})) is not None:
            return serialize_collection(existing_trailer)
    
    raise HTTPException(status_code=500, detail="Failed to update repairs")

@app.delete("/trailers/{trailer_id}", response_description="Delete a trailer")
async def delete_trailer(trailer_id: str):
    
    collection = db.get_collection("trailers")
    
    delete_result = collection.delete_one({"_id": ObjectId(trailer_id)})
    if delete_result.deleted_count == 1:
        return {"response": "trailer Deleted 204"}

    return({"status_code": 404, "detail": f"trailer {trailer_id} not found"})




#Truck Driver API Paths


@app.get("/truck_drivers/")
async def get_truck_drivers():
    try:
        collection = db.get_collection("truck_drivers")
        truck_drivers = list(collection.find())
        
        return {"serialized_truck_drivers": serialize_collection(truck_drivers)}
    except Exception as e:
        print("An error occurred:", str(e))


@app.get("/truck_drivers/{truck_driver_id}")
async def get_truck_driver(
    truck_driver_id: Annotated[str, Path(title= "id of object to get")]
):
    try:
        collection = db.get_collection("truck_drivers")
        truck_driver = collection.find_one({"_id": ObjectId(truck_driver_id)})
        
        return {"serialized_truck_driver": serialize_collection(truck_driver)}
    except Exception as e:
        print("An error occurred:", str(e))

@app.post("/truck_drivers/", response_description="Add new Truck driver", response_model=TruckDriver)
async def create_truck_driver(truck_driver: TruckDriver = Body(...)):
    try:
        truck_driver = jsonable_encoder(truck_driver)
        if "_id" in truck_driver:
            del truck_driver["_id"]

        collection = db.get_collection("truck_drivers")

        new_truck_driver = collection.insert_one(truck_driver)
        created_truck_driver = collection.find_one({"_id": ObjectId(new_truck_driver.inserted_id)})
        serialized_truck_driver = serialize_collection(created_truck_driver)
        print({"serialized_truck_driver": serialized_truck_driver})
        return serialized_truck_driver
    except Exception as e:
        print("An error occurred:", str(e))

@app.patch("/truck_drivers/{truck_driver_id}", response_description="Update a Truck driver", response_model=TruckDriver)
async def update_truck_driver(truck_driver_id: str, truck_driver_updates: UpdateTruckDriverModel = Body(...)):
    truck_driver_updates = {k: v for k, v in truck_driver_updates.dict().items() if v is not None}

    collection = db.get_collection("truck_drivers")
    truck_driver = collection.find_one({"_id": ObjectId(truck_driver_id)})
    if truck_driver is None:
        raise HTTPException(status_code=404, detail="Truck driver not found")
    
    if len(truck_driver_updates) >= 1:
        collection.update_one({"_id": ObjectId(truck_driver_id)}, {"$set": truck_driver_updates})

    if (existing_truck_driver := collection.find_one({"_id": ObjectId(truck_driver_id)})) is not None:
        return serialize_collection(existing_truck_driver)

@app.delete("/truck_drivers/{truck_driver_id}", response_description="Delete a truck driver")
async def delete_truck_driver(truck_driver_id: str):
    
    collection = db.get_collection("truck_drivers")
    
    delete_result = collection.delete_one({"_id": ObjectId(truck_driver_id)})
    if delete_result.deleted_count == 1:
        return {"response": "Truck driver Deleted 204"}

    return({"status_code": 404, "detail": f"Truck driver {truck_driver_id} not found"})




# Manager API Paths:



@app.get("/managers/")
async def get_managers():
    try:
        collection = db.get_collection("managers")
        managers = list(collection.find())
        
        return {"serialized_managers": serialize_collection(managers)}
    except Exception as e:
        print("An error occurred:", str(e))


@app.get("/managers/{manager_id}")
async def get_manager(
    manager_id: Annotated[str, Path(title= "id of object to get")]
):
    try:
        collection = db.get_collection("managers")
        manager = collection.find_one({"_id": ObjectId(manager_id)})
        
        return {"serialized_manager": serialize_collection(manager)}
    except Exception as e:
        print("An error occurred:", str(e))

@app.post("/managers/", response_description="Add new manager", response_model=Manager)
async def create_manager(manager: Manager = Body(...)):
    try:
        manager = jsonable_encoder(manager)
        if "_id" in manager:
            del manager["_id"]

        collection = db.get_collection("managers")

        new_manager = collection.insert_one(manager)
        created_manager = collection.find_one({"_id": ObjectId(new_manager.inserted_id)})
        serialized_manager = serialize_collection(created_manager)
        print({"serialized_manager": serialized_manager})
        return serialized_manager
    except Exception as e:
        print("An error occurred:", str(e))

@app.patch("/managers/{manager_id}", response_description="Update a manager", response_model=Manager)
async def update_manager(manager_id: str, manager_updates: UpdateManagerModel = Body(...)):
    manager_updates = {k: v for k, v in manager_updates.dict().items() if v is not None}

    collection = db.get_collection("managers")
    manager = collection.find_one({"_id": ObjectId(manager_id)})
    if manager is None:
        raise HTTPException(status_code=404, detail="Manager not found")
    
    if len(manager_updates) >= 1:
        collection.update_one({"_id": ObjectId(manager_id)}, {"$set": manager_updates})

    if (existing_manager := collection.find_one({"_id": ObjectId(manager_id)})) is not None:
        return serialize_collection(existing_manager)

@app.delete("/managers/{manager_id}", response_description="Delete a manager")
async def delete_manager(manager_id: str):
    
    collection = db.get_collection("managers")
    
    delete_result = collection.delete_one({"_id": ObjectId(manager_id)})
    if delete_result.deleted_count == 1:
        return {"response": "Manager Deleted 204"}

    return({"status_code": 404, "detail": f"Manager {manager_id} not found"})





#Dispatcher API Paths



@app.get("/dispatchers/")
async def get_dispatchers():
    try:
        collection = db.get_collection("dispatchers")
        dispatchers = list(collection.find())
        
        return {"serialized_dispatchers": serialize_collection(dispatchers)}
    except Exception as e:
        print("An error occurred:", str(e))


@app.get("/dispatchers/{dispatcher_id}")
async def get_dispatcher(
    dispatcher_id: Annotated[str, Path(title= "id of object to get")]
):
    try:
        collection = db.get_collection("dispatchers")
        dispatcher = collection.find_one({"_id": ObjectId(dispatcher_id)})
        
        return {"serialized_dispatcher": serialize_collection(dispatcher)}
    except Exception as e:
        print("An error occurred:", str(e))

@app.post("/dispatchers/", response_description="Add new Truck driver", response_model=Dispatcher)
async def create_dispatcher(dispatcher: Dispatcher = Body(...)):
    try:
        dispatcher = jsonable_encoder(dispatcher)
        if "_id" in dispatcher:
            del dispatcher["_id"]

        collection = db.get_collection("dispatchers")

        new_dispatcher = collection.insert_one(dispatcher)
        created_dispatcher = collection.find_one({"_id": ObjectId(new_dispatcher.inserted_id)})
        serialized_dispatcher = serialize_collection(created_dispatcher)
        print({"serialized_dispatcher": serialized_dispatcher})
        return serialized_dispatcher
    except Exception as e:
        print("An error occurred:", str(e))

@app.patch("/dispatchers/{dispatcher_id}", response_description="Update a Truck driver", response_model=Dispatcher)
async def update_dispatcher(dispatcher_id: str, dispatcher_updates: UpdateDispatcherModel = Body(...)):
    dispatcher_updates = {k: v for k, v in dispatcher_updates.dict().items() if v is not None}

    collection = db.get_collection("dispatchers")
    dispatcher = collection.find_one({"_id": ObjectId(dispatcher_id)})
    if dispatcher is None:
        raise HTTPException(status_code=404, detail="Truck driver not found")
    
    if len(dispatcher_updates) >= 1:
        collection.update_one({"_id": ObjectId(dispatcher_id)}, {"$set": dispatcher_updates})

    if (existing_dispatcher := collection.find_one({"_id": ObjectId(dispatcher_id)})) is not None:
        return serialize_collection(existing_dispatcher)

@app.delete("/dispatchers/{dispatcher_id}", response_description="Delete a truck driver")
async def delete_dispatcher(dispatcher_id: str):
    
    collection = db.get_collection("dispatchers")
    
    delete_result = collection.delete_one({"_id": ObjectId(dispatcher_id)})
    if delete_result.deleted_count == 1:
        return {"response": "Truck driver Deleted 204"}

    return({"status_code": 404, "detail": f"Truck driver {dispatcher_id} not found"})

#TODO Finish PUT paths for manager and dispatcher, and fix what props are optional for truck driver and dispatcher



