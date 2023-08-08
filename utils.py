def serialize_collection(collection):
    if isinstance(collection, list):
        serialized_collection = []
        for obj in collection:
            obj_dict = obj.copy()
            obj_dict["_id"] = str(obj["_id"])
            serialized_collection.append(obj_dict)
        return serialized_collection
    elif isinstance(collection, dict):
        obj_dict = collection.copy()
        obj_dict["_id"] = str(collection["_id"])
        return obj_dict