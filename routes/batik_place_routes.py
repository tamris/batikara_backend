from flask import Blueprint, render_template, request, redirect, url_for, current_app
from bson.objectid import ObjectId

batik_place_bp = Blueprint("batik_place_bp", __name__, template_folder="../templates/batik_places")

@batik_place_bp.route("/batik-places")
def index():
    places = list(current_app.mongo.db.batik_places.find())
    return render_template("index.html", places=places)

@batik_place_bp.route("/batik-places/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"]
        lat = float(request.form["latitude"])
        lng = float(request.form["longitude"])
        desc = request.form["description"]

        current_app.mongo.db.batik_places.insert_one({
            "name": name,
            "latitude": lat,
            "longitude": lng,
            "description": desc
        })
        return redirect(url_for("batik_place_bp.index"))

    return render_template("create.html")

@batik_place_bp.route("/batik-places/edit/<id>", methods=["GET", "POST"])
def edit(id):
    place = current_app.mongo.db.batik_places.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        current_app.mongo.db.batik_places.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "name": request.form["name"],
                "latitude": float(request.form["latitude"]),
                "longitude": float(request.form["longitude"]),
                "description": request.form["description"]
            }}
        )
        return redirect(url_for("batik_place_bp.index"))

    return render_template("edit.html", place=place)

@batik_place_bp.route("/batik-places/delete/<id>")
def delete(id):
    current_app.mongo.db.batik_places.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("batik_place_bp.index"))

# Endpoint untuk Flutter
@batik_place_bp.route("/api/batik-places", methods=["GET"])
def api_get_batik_places():
    places = list(current_app.mongo.db.batik_places.find({}, {"_id": 0}))
    return {"places": places}
