from flask import Blueprint, render_template, redirect, current_app

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/admin/dashboard")
def admin_dashboard():
    mongo = current_app.mongo
    db = mongo.db

    user_count = db.users.count_documents({})
    batik_count = db.gallery.count_documents({})
    article_count = db.articles.count_documents({})
    event_count = db.events.count_documents({})
    video_count = db.videos.count_documents({})
    mapping_count = db.batik_places.count_documents({})

    # DEBUG PRINT
    print("batik_count =", batik_count)

    return render_template("dashboard.html",
        user_count=user_count,
        batik_count=batik_count,
        article_count=article_count,
        event_count=event_count,
        video_count=video_count,
        mapping_count=mapping_count
    )





@dashboard_bp.route("/")
def home():
    return redirect("/admin/dashboard")
