import os
from bson import ObjectId
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
# from werkzeug.security import check_password_hash, generate_password_hash


user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = current_app.mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"message": "User tidak ditemukan"}), 404

    # Hindari mengirim password ke client
    user.pop("password", None)
    user["_id"] = str(user["_id"])  # Konversi ObjectId ke string
    return jsonify(user), 200


@user_bp.route("/profile/edit", methods=["PUT"])
@jwt_required()
def edit_profile():
    user_id = get_jwt_identity()

    # Ambil data dari form
    username = request.form.get("username")
    gender = request.form.get("gender")
    tanggal_lahir = request.form.get("tanggal_lahir")
    profile_picture_file = request.files.get("profile_picture")

    update_fields = {}

    if username:
        update_fields["username"] = username
    if gender:
        update_fields["gender"] = gender
    if tanggal_lahir:
        update_fields["tanggal_lahir"] = tanggal_lahir

    if profile_picture_file:
        filename = secure_filename(profile_picture_file.filename)
        upload_path = current_app.config["UPLOAD_FOLDER_PROFILE"]  # ✅ Ambil dari config.py
        os.makedirs(upload_path, exist_ok=True)

        file_path = os.path.join(upload_path, filename)
        profile_picture_file.save(file_path)

        # Simpan path (atau URL jika kamu serve sebagai public)
        update_fields["profile_picture"] = f"/{file_path}"

    if not update_fields:
        return jsonify({"message": "No fields to update"}), 400

    result = current_app.mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_fields}
    )

    if result.matched_count == 0:
        return jsonify({"message": "User tidak ditemukan"}), 404

    return jsonify({"message": "Profile updated successfully"}), 200


@user_bp.route("/profile/delete", methods=["DELETE"])
@jwt_required()
def delete_profile():
    user_id = get_jwt_identity()

    result = current_app.mongo.db.users.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count == 0:
        return jsonify({"message": "User tidak ditemukan"}), 404

    return jsonify({"message": "User deleted successfully"}), 200


@user_bp.route("/profile/change-password", methods=["POST"])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    data = request.get_json()

    current_password = data.get("current_password")
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    # Validasi input
    if not current_password or not new_password or not confirm_password:
        return jsonify({"message": "Semua field wajib diisi"}), 400

    if new_password != confirm_password:
        return jsonify({"message": "Password baru dan konfirmasi tidak cocok"}), 400

    # Ambil user dari DB
    user = current_app.mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"message": "User tidak ditemukan"}), 404

    bcrypt = current_app.bcrypt

    # Pastikan password lama cocok
    if not bcrypt.check_password_hash(user["password"], current_password):
        return jsonify({"message": "Password saat ini salah"}), 401

    # Hash password baru
    hashed_pw = bcrypt.generate_password_hash(new_password).decode('utf-8')

    # Update ke DB
    current_app.mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"password": hashed_pw}}
    )

    return jsonify({"message": "Password berhasil diubah"}), 200

