import os
from werkzeug.utils import secure_filename
from flask import current_app, request

# Serializer untuk JSON / web

def gallery_serializer(gallery):
    raw_image_path = gallery.get("image", "").replace("\\", "/")
    full_image_url = f"{request.host_url.rstrip('/')}{raw_image_path}"

    return {
        "id": str(gallery["_id"]),
        "nama_batik": gallery.get("nama_batik", ""),
        "deskripsi": gallery.get("deskripsi", ""),
        "image": full_image_url
    }

# Proses data dari form POST create
def create_gallery_data(form, image_file):
    filename = secure_filename(image_file.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER_GALLERY']
    image_path = os.path.join(upload_folder, filename)
    image_file.save(image_path)
    image_url = f"/{image_path}"

    return {
        "nama_batik": form.get("nama_batik"),
        "deskripsi": form.get("deskripsi"),
        "image": image_url
    }

# Proses data dari form POST edit
def update_gallery_data(form, image_file=None):
    update_data = {
        "nama_batik": form.get("nama_batik"),
        "deskripsi": form.get("deskripsi")
    }

    if image_file and image_file.filename:
        filename = secure_filename(image_file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER_GALLERY']
        image_path = os.path.join(upload_folder, filename)
        image_file.save(image_path)
        update_data["image"] = f"/{image_path}"

    return update_data
