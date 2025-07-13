from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from bson import ObjectId
import os
from models.event_model import (
    get_all_events,
    get_event_by_id,
    create_event,
    update_event,
    delete_event
)

event_bp = Blueprint("event_web", __name__)

# ========================
# Halaman Index Event
# ========================
@event_bp.route("/admin/event")
def event_index():
    if session.get("role") != "admin":
        return redirect(url_for("auth_web.login"))

    events = get_all_events()
    return render_template("event/index.html", events=events)

# ========================
# Buat Event
# ========================
@event_bp.route("/admin/event/create", methods=["GET", "POST"])
def create_event_route():
    if session.get("role") != "admin":
        return redirect(url_for("auth_web.login"))

    if request.method == "POST":
        judul = request.form.get("judul")
        waktu = request.form.get("waktu")
        lokasi = request.form.get("lokasi")
        deskripsi = request.form.get("deskripsi")
        foto = request.files.get("foto")

        filename = ""
        if foto:
            filename = foto.filename
            path = os.path.join("static/uploads", filename)
            foto.save(path)

        create_event({
            "judul": judul,
            "waktu": waktu,
            "lokasi": lokasi,
            "deskripsi": deskripsi,
            "foto": filename
        })

        flash("Event berhasil ditambahkan!", "success")
        return redirect(url_for("event_web.event_index"))

    return render_template("event/create.html")

# ========================
# Edit Event
# ========================
@event_bp.route("/admin/event/edit/<id>", methods=["GET", "POST"])
def edit_event_route(id):
    if session.get("role") != "admin":
        return redirect(url_for("auth_web.login"))

    event = get_event_by_id(id)
    if not event:
        return "Event tidak ditemukan", 404

    if request.method == "POST":
        judul = request.form.get("judul")
        waktu = request.form.get("waktu")
        lokasi = request.form.get("lokasi")
        deskripsi = request.form.get("deskripsi")
        foto = request.files.get("foto")

        update_data = {
            "judul": judul,
            "waktu": waktu,
            "lokasi": lokasi,
            "deskripsi": deskripsi
        }

        if foto:
            filename = foto.filename
            path = os.path.join("static/uploads", filename)
            foto.save(path)
            update_data["foto"] = filename

        update_event(id, update_data)
        flash("Event berhasil diperbarui!", "success")
        return redirect(url_for("event_web.event_index"))

    return render_template("event/edit.html", event=event)

# ========================
# Hapus Event
# ========================
@event_bp.route("/admin/event/delete/<id>")
def delete_event_route(id):
    if session.get("role") != "admin":
        return redirect(url_for("auth_web.login"))

    delete_event(id)
    flash("Event berhasil dihapus!", "info")
    return redirect(url_for("event_web.event_index"))
