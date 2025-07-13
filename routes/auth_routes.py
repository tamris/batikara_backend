from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models.user_log import get_login_logs_by_user, save_login_log
from models.user_model import create_user, find_user_by_email
from utils.email_utils import send_email, generate_otp
from models.otp_model import save_otp, verify_otp
from datetime import datetime, timedelta
import secrets

auth_bp = Blueprint("auth", __name__)

#register
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if find_user_by_email(data["email"]):
        return jsonify({"msg": "User already exists"}), 409
    
    api_key = secrets.token_hex(16)
    data["api_key"] = api_key
    
    # Buat user (sebelum verifikasi)
    create_user(data)
    
    # Kirim OTP untuk verifikasi email
    save_otp(data["email"])
    
    return jsonify({"msg": "User created, OTP sent for verification"}), 201

#verify-email
@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp_route():
    data = request.get_json()
    if verify_otp(data["email"], data["otp"]):
        return jsonify({"msg": "OTP verified successfully"}), 200
    return jsonify({"msg": "Invalid or expired OTP"}), 400

#resend otp email
@auth_bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    data = request.get_json()
    email = data.get('email')

    user = find_user_by_email(email)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    if user.get('is_verified'):
        return jsonify({"msg": "Email already verified"}), 400

    otp = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    current_app.mongo.db.otp_verifications.update_one(
        {"email": email},
        {"$set": {
            "otp": otp,
            "expires_at": expires_at,
            "verified": False  # pastikan ini direset ke False
        }},
        upsert=True
    )

    # Panggil fungsi kirim email dengan parameter yang benar
    send_email(email, otp)

    return jsonify({"msg": "OTP has been resent"}), 200

# login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = find_user_by_email(data["email"])
    
    bcrypt = current_app.bcrypt

    if not user:
        return jsonify({"msg": "Invalid email or password"}), 401

    if not user.get("is_verified", False):
        return jsonify({"msg": "Please verify your email before logging in."}), 403

    if bcrypt.check_password_hash(user["password"], data["password"]):
        access_token = create_access_token(identity=str(user["_id"]))

        # Ambil dari body JSON dulu, fallback ke User-Agent jika tidak ada
        device = data.get("device_name") or request.headers.get("User-Agent", "unknown")

        # Simpan riwayat login
        save_login_log(user["_id"], device)

        return jsonify({
            "access_token": access_token,
            "api_key": user.get("api_key", None)
        }), 200

    return jsonify({"msg": "Invalid email or password"}), 401

#login history
@auth_bp.route("/login-history", methods=["GET"])
@jwt_required()
def get_login_history():
    user_id = get_jwt_identity()
    history = get_login_logs_by_user(user_id)
    return jsonify(history), 200
