from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from config import Config
from models.user_log import save_login_log
from models.user_model import find_user_by_email, create_user
import secrets

google_auth_bp = Blueprint('google_auth', __name__)
GOOGLE_CLIENT_ID = Config.GOOGLE_CLIENT_ID

@google_auth_bp.route("/auth/google", methods=["POST"])
def login_with_google():
    data = request.get_json()
    token = request.json.get("token")

    try:
        idinfo = id_token.verify_oauth2_token(token, grequests.Request(), GOOGLE_CLIENT_ID)

        email = idinfo.get("email")
        name = idinfo.get("name")

        user = find_user_by_email(email)

        if not user:
            user_data = {
                "username": name,
                "email": email,
                "password": secrets.token_hex(16), 
                "api_key": secrets.token_hex(16),
                "oauth_provider": "google",
                "is_verified": True
            }
            create_user(user_data)
            user = find_user_by_email(email)  # Fetch ulang setelah dibuat

        access_token = create_access_token(identity=str(user["_id"]))

        # ✅ Simpan riwayat login
        device_info = data.get("device_name") or request.headers.get("User-Agent", "unknown")
        save_login_log(user["_id"], device_info)

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "email": email,
            "api_key": user.get("api_key")
        }), 200

    except ValueError:
        return jsonify({"error": "Invalid token"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
