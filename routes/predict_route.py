from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from bson import ObjectId
from flask import current_app
from PIL import Image
import numpy as np
import io

from models.batik_model import model, label_kelas
from utils.motif_makna import motif_makna  # makna motif

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['POST'])
@jwt_required()
def predict_image():
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "Tidak ada file terlampir"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "Nama file kosong"}), 400

        image = Image.open(io.BytesIO(file.read())).convert("RGB")
        image = image.resize((128, 128))
        img_array = np.expand_dims(np.array(image), axis=0).astype("float32") / 255.0

        predictions = model.predict(img_array)
        predicted_class = int(np.argmax(predictions, axis=1)[0])
        label = label_kelas[predicted_class]
        confidence = float(np.max(predictions))

        makna = motif_makna.get(label, "Makna untuk motif ini belum tersedia.")

        # Simpan ke MongoDB jika tidak duplikat dalam 5 detik terakhir
        user_id = get_jwt_identity()
        db = current_app.mongo.db
        five_seconds_ago = datetime.utcnow() - timedelta(seconds=5)
        existing = db.detection_history.find_one({
            "user_id": ObjectId(user_id),
            "label": label,
            "timestamp": {"$gte": five_seconds_ago}
        })

        if not existing:
            db.detection_history.insert_one({
                "user_id": ObjectId(user_id),
                "label": label,
                "confidence": confidence,
                "timestamp": datetime.utcnow()
            })

        return jsonify({
            "success": True,
            "label": label,
            "confidence": round(confidence, 4),
            "makna": makna
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



@predict_bp.route('/riwayat', methods=['GET'])
@jwt_required()
def get_riwayat():
    try:
        user_id = get_jwt_identity()
        db = current_app.mongo.db

        riwayat = list(db.detection_history.find(
            {"user_id": ObjectId(user_id)}
        ).sort("timestamp", -1))  # urut terbaru dulu

        hasil = []
        for item in riwayat:
            hasil.append({
                "id": str(item["_id"]),
                "label": item["label"],
                "confidence": round(item["confidence"], 4),
                "timestamp": item["timestamp"].isoformat()
            })

        return jsonify({
            "success": True,
            "data": hasil
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@predict_bp.route('/detection/stats', methods=['GET'])
@jwt_required()
def detection_stats():
    try:
        user_id = get_jwt_identity()
        db = current_app.mongo.db

        pipeline = [
            {"$match": {"user_id": ObjectId(user_id)}},
            {"$group": {"_id": "$label", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
        ]

        results = list(db.detection_history.aggregate(pipeline))

        return jsonify({
            "success": True,
            "data": [{"label": r["_id"], "count": r["count"]} for r in results]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
