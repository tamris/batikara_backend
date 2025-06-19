from flask import current_app
from datetime import datetime, timedelta
import random
from utils.email_utils import send_email

# Fungsi untuk menyimpan OTP ke database dan mengirimkannya ke email pengguna
def save_otp(email):
    # Hapus OTP yang sudah diverifikasi atau expired sebelumnya
    current_app.mongo.db.otp_verifications.delete_many({"email": email, "verified": True})
    
    # Generate OTP baru
    otp = str(random.randint(100000, 999999))  # 6 digit angka OTP
    
    # Tentukan waktu kedaluwarsa OTP (5 menit dari sekarang)
    expiration = datetime.utcnow() + timedelta(minutes=5)
    
    # Simpan OTP baru ke database
    current_app.mongo.db.otp_verifications.insert_one({
        "email": email,
        "otp": otp,
        "expires_at": expiration,
        "verified": False
    })
    
    # Kirim OTP ke email pengguna
    send_email(email, otp)

# Fungsi untuk memverifikasi OTP yang dimasukkan pengguna
def verify_otp(email, otp_input):
    # Cari record OTP yang sesuai berdasarkan email dan OTP yang dimasukkan
    record = current_app.mongo.db.otp_verifications.find_one({"email": email, "otp": otp_input})
    
    # Jika OTP valid, belum terverifikasi, dan belum expired
    if record and not record["verified"] and record["expires_at"] > datetime.utcnow():
        # Tandai OTP sebagai terverifikasi
        current_app.mongo.db.otp_verifications.update_one(
            {"_id": record["_id"]},
            {"$set": {"verified": True}}
        )
        
        # Update status is_verified pada user menjadi True setelah OTP diverifikasi
        current_app.mongo.db.users.update_one(
            {"email": email},
            {"$set": {"is_verified": True}}
        )
        
        return True
    
    # Jika OTP tidak valid, expired, atau sudah diverifikasi
    return False
