from flask import current_app
from datetime import datetime, timedelta
import random
from utils.email_utils import send_email

def save_otp(email, purpose="verify"):
    # Hapus OTP lama yang sudah verified (optional)
    current_app.mongo.db.otp_verifications.delete_many({
        "email": email,
        "verified": True,
        "purpose": purpose
    })

    otp = str(random.randint(100000, 999999))
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    current_app.mongo.db.otp_verifications.insert_one({
        "email": email,
        "otp": otp,
        "expires_at": expires_at,
        "verified": False,
        "purpose": purpose  # NEW: tandai tujuan OTP ini
    })

    send_email(email, otp)

def verify_otp(email, otp_input, purpose="verify"):
    record = current_app.mongo.db.otp_verifications.find_one({
        "email": email,
        "otp": otp_input,
        "purpose": purpose
    })

    if record and not record["verified"] and record["expires_at"] > datetime.utcnow():
        current_app.mongo.db.otp_verifications.update_one(
            {"_id": record["_id"]},
            {"$set": {"verified": True}}
        )

        if purpose == "verify":
            current_app.mongo.db.users.update_one(
                {"email": email},
                {"$set": {"is_verified": True}}
            )

        return True

    return False
