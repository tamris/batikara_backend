from flask import current_app
from bson import ObjectId
from datetime import datetime
from zoneinfo import ZoneInfo

def save_login_log(user_id, device):
    current_app.mongo.db.login_logs.insert_one({
        "user_id": ObjectId(user_id),
        "device": device,
        "login_time": datetime.utcnow()
    })


def get_login_logs_by_user(user_id):
    logs = current_app.mongo.db.login_logs.find(
        {"user_id": ObjectId(user_id)},
        {"_id": 0, "device": 1, "login_time": 1}
    ).sort("login_time", -1)

    return [
        {
            "device": log["device"],
            "login_time": log["login_time"].replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S")
        } for log in logs
    ]
