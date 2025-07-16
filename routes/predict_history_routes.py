from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson.objectid import ObjectId
from flask import current_app

history_bp = Blueprint("history", __name__, url_prefix="/history")

@history_bp.route("/save", methods=["POST"])
@jwt_required()
def save_detection():
    data = request.get_json()
    user_id = get_jwt_identity()

    required_fields = ["label", "makna", "confidence"]
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Incomplete data"}), 400

    new_history = {
        "user_id": ObjectId(user_id),
        "label": data["label"],
        "makna": data["makna"],
        "confidence": data["confidence"],
        "timestamp": datetime.utcnow()
    }

    db = current_app.mongo.db
    db.detection_history.insert_one(new_history)

    return jsonify({"msg": "Detection history saved"}), 201
