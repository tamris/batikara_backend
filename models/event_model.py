from flask import current_app
from bson import ObjectId

def get_all_events():
    return list(current_app.mongo.db.events.find())

def get_event_by_id(event_id):
    return current_app.mongo.db.events.find_one({"_id": ObjectId(event_id)})

def create_event(data):
    return current_app.mongo.db.events.insert_one(data)

def update_event(event_id, update_data):
    return current_app.mongo.db.events.update_one(
        {"_id": ObjectId(event_id)},
        {"$set": update_data}
    )

def delete_event(event_id):
    return current_app.mongo.db.events.delete_one({"_id": ObjectId(event_id)})
