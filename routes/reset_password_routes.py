import bcrypt
from flask import Blueprint, request, jsonify, current_app
from models.user_model import find_user_by_email, update_user_password
from models.otp_model import save_otp, verify_otp

reset_bp = Blueprint("reset", __name__)

@reset_bp.route("/reset/request", methods=["POST"])
def request_reset():
    data = request.get_json()
    email = data.get("email")

    user = find_user_by_email(email)
    if not user:
        return jsonify({"msg": "Email tidak ditemukan"}), 404

    # Kirim OTP khusus untuk reset password
    save_otp(email, purpose="reset")

    return jsonify({"msg": "OTP terkirim ke email"}), 200


@reset_bp.route("/reset/verify", methods=["POST"])
def verify_reset():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")

    if verify_otp(email, otp, purpose="reset"):
        return jsonify({"msg": "OTP valid"}), 200
    return jsonify({"msg": "OTP tidak valid atau sudah kadaluarsa"}), 400


@reset_bp.route("/reset/confirm", methods=["POST"])
def confirm_new_password():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    verification = current_app.mongo.db.otp_verifications.find_one({
        "email": email,
        "verified": True,
        "purpose": "reset"
    })

    if not verification:
        return jsonify({"msg": "OTP belum diverifikasi"}), 403

    # Hash pakai bcrypt (biar konsisten sama saat registrasi)
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    update_user_password(email, hashed_pw)

    current_app.mongo.db.otp_verifications.delete_one({"_id": verification["_id"]})

    return jsonify({"msg": "Password berhasil diubah"}), 200

