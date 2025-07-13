from flask import current_app

def create_user(data):
    bcrypt = current_app.bcrypt
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    user = {
        "username": data["username"],
        "email": data["email"],
        "password": hashed_password,
        "api_key": data["api_key"],
        "is_verified": data.get("is_verified", False),  # ✅ Pakai nilai dari data kalau ada
        "oauth_provider": data.get("oauth_provider", None),  # opsional, biar aman
        "profile_picture": data.get("profile_picture", ""),
        "gender": data.get("gender", ""),  # 👈 Tambahan gender
        "tanggal_lahir": data.get("tanggal_lahir", "")  # 👈 Tambahan tanggal lahir
    }
    current_app.mongo.db.users.insert_one(user)
    return user

def find_user_by_email(email):
    return current_app.mongo.db.users.find_one({"email": email})


def update_user_password(email, new_password_hash):
    current_app.mongo.db.users.update_one(
        {"email": email},
        {"$set": {"password": new_password_hash}}
    )