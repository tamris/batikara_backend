from flask import current_app
from bson import ObjectId

def get_all_videos():
    return list(current_app.mongo.db.videos.find())

def get_video_by_id(video_id):
    return current_app.mongo.db.videos.find_one({'_id': ObjectId(video_id)})

def insert_video(data):
    return current_app.mongo.db.videos.insert_one(data)

def update_video(video_id, data):
    return current_app.mongo.db.videos.update_one({'_id': ObjectId(video_id)}, {'$set': data})

def delete_video(video_id):
    return current_app.mongo.db.videos.delete_one({'_id': ObjectId(video_id)})
