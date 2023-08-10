from get_db_pymongo import get_database

def get_trucks_collection():
    db = get_database()
    return db.get_collection("trucks")

def get_trailers_collection():
    db = get_database()
    return db.get_collection("trailers")

def get_managers_collection():
    db = get_database()
    return db.get_collection("managers")

def get_dispatchers_collection():
    db = get_database()
    return db.get_collection("dispatchers")

def get_truck_drivers_collection():
    db = get_database()
    return db.get_collection("truck_drivers")