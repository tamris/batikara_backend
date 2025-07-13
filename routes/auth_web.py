from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
# from config import admin_col, user_col
from flask import current_app

auth_web_bp = Blueprint("auth_web", __name__)

# ========================
# DEFAULT: Landing awal
# ========================
@auth_web_bp.route("/")
def index():
    role = session.get("role")
    return render_template("landing.html", role=role)


# ========================
# LOGIN: Admin & User
# ========================
@auth_web_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        print("🧪 Form input:", username, password)

        if not username or not password:
            flash("Semua field wajib diisi.", "warning")
            return redirect(url_for("auth_web.login"))

        mongo = current_app.mongo
        admin_col = mongo.db.admin
        user_col = mongo.db.user

        # Cek admin
        admin = admin_col.find_one({"username": username})
        print("🔍 Admin ditemukan:", admin)

        if admin and check_password_hash(admin["password"], password):
            session["username"] = username
            session["role"] = "admin"
            print("✅ Login berhasil sebagai ADMIN:", username)
            flash("Login Admin berhasil!", "success")
            return redirect(url_for("auth_web.admin_dashboard"))

        # Cek user
        user = user_col.find_one({"username": username})
        print("🔍 User ditemukan:", user)

        if user and check_password_hash(user["password"], password):
            session["username"] = username
            session["role"] = "user"
            print("✅ Login berhasil sebagai USER:", username)
            flash("Login User berhasil!", "success")
            return redirect(url_for("auth_web.landing"))

        print("❌ Login gagal. Tidak cocok sebagai admin maupun user.")
        flash("Username atau password salah!", "error")
        return redirect(url_for("auth_web.login"))

    return render_template("auth.html", mode="login")


# ========================
# REGISTRASI (user)
# ========================
@auth_web_bp.route("/regist", methods=["GET", "POST"])
def regist():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not username or not email or not password:
            flash("Semua field wajib diisi.", "warning")
            return redirect(url_for("auth_web.regist"))
        
         # ⬇️ Taruh di sini juga
        mongo = current_app.mongo
        admin_col = mongo.db.admin
        user_col = mongo.db.user

        # Cek apakah username sudah ada
        if admin_col.find_one({"username": username}) or user_col.find_one({"username": username}):
            flash("Username sudah terdaftar!", "warning")
            return redirect(url_for("auth_web.regist"))

        user_col.insert_one({
            "username": username,
            "email": email,
            "password": generate_password_hash(password)
        })

        flash("Registrasi berhasil. Silakan login.", "success")
        return redirect(url_for("auth_web.login"))

    return render_template("auth.html", mode="regist")


# ========================
# DASHBOARD ADMIN (dengan data jumlah)
# ========================
@auth_web_bp.route("/admin/dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        flash("Akses ditolak. Login sebagai admin.", "error")
        return redirect(url_for("auth_web.login"))

    # Hitung data dari masing-masing koleksi
    mongo = current_app.mongo
    user_count = mongo.db.users.count_documents({})
    batik_count = mongo.db.gallery.count_documents({})
    artikel_count = mongo.db.articles.count_documents({})
    event_count = mongo.db.events.count_documents({})  
    video_count = mongo.db.videos.count_documents({})  
    mapping_count = mongo.db.batik_places.count_documents({})  

    return render_template(
        "dashboard.html",
        user_count=user_count,
        batik_count=batik_count,
        article_count=artikel_count,
        event_count=event_count,
        video_count=video_count,
        mapping_count=mapping_count
    )


# ========================
# LANDING PAGE
# ========================
@auth_web_bp.route("/landing")
def landing():
    role = session.get("role")
    return render_template("landing.html", role=role)


# ========================
# LOGOUT
# ========================
@auth_web_bp.route("/logout")
def logout():
    session.clear()
    flash("Anda berhasil logout.", "info")
    return redirect(url_for("auth_web.index"))
