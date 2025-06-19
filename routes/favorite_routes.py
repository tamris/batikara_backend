from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from models.gallery_model import gallery_serializer
from flask_jwt_extended import jwt_required, get_jwt_identity


favorite_bp = Blueprint("favorite_bp", __name__)

@favorite_bp.route('/favorites', methods=['GET'])
@jwt_required()
def get_user_favorites():
    user_id = get_jwt_identity()

    user = current_app.mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404

    favorite_ids = user.get("favorites", [])
    galleries = current_app.mongo.db.gallery.find({"_id": {"$in": [ObjectId(fid) for fid in favorite_ids]}})
    return jsonify([gallery_serializer(g) for g in galleries]), 200



@favorite_bp.route('/favorites/toggle', methods=['POST'])
@jwt_required()
def toggle_favorite():
    user_id = get_jwt_identity()
    data = request.get_json()
    gallery_id = data.get('gallery_id')

    if not gallery_id:
        return jsonify({"error": "Gallery ID is required"}), 400

    user = current_app.mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404

    favorites = user.get("favorites", [])
    if gallery_id in favorites:
        favorites.remove(gallery_id)
    else:
        favorites.append(gallery_id)

    current_app.mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'favorites': favorites}})
    return jsonify({"success": True, "favorites": favorites}), 200

