from flask import Blueprint, flash, redirect, render_template, request, jsonify, current_app, url_for
from werkzeug.utils import secure_filename
from models.article_model import article_serializer, create_article_data
from bson import ObjectId
import os

article_bp = Blueprint('article', __name__)

# READ - Flutter pakai endpoint ini
@article_bp.route('/articles', methods=['GET'])
def get_articles():
    articles = current_app.mongo.db.articles.find()
    return jsonify([article_serializer(a) for a in articles]), 200


# TAMPILKAN ARTIKEL
@article_bp.route('/web/articles')
def web_article_index():
    articles = current_app.mongo.db.articles.find()
    return render_template('articles/index.html', articles=[article_serializer(a) for a in articles])

# FORM TAMBAH ARTIKEL
@article_bp.route('/web/articles/create', methods=['GET', 'POST'])
def web_article_create():
    if request.method == 'POST':
        title = request.form.get("title")
        description = request.form.get("description")
        image = request.files.get("image")

        if not image:
            flash("Image is required", "danger")
            return redirect(request.url)

        filename = secure_filename(image.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        image_path = os.path.join(upload_folder, filename)
        image.save(image_path)
        image_url = f"/{image_path}"

        article = create_article_data(title, description, image_url)
        current_app.mongo.db.articles.insert_one(article)
        return redirect(url_for('article.web_article_index'))   

    return render_template('articles/create.html')

# FORM EDIT ARTIKEL
@article_bp.route('/web/articles/edit/<id>', methods=['GET', 'POST'])
def web_article_edit(id):
    article = current_app.mongo.db.articles.find_one({"_id": ObjectId(id)})
    if not article:
        return "Not found", 404

    if request.method == 'POST':
        title = request.form.get("title")
        description = request.form.get("description")
        image = request.files.get("image")

        update_data = {
            "title": title,
            "description": description
        }

        if image:
            filename = secure_filename(image.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            image_path = os.path.join(upload_folder, filename)
            image.save(image_path)
            update_data["image_url"] = f"/{image_path}"

        current_app.mongo.db.articles.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        return redirect(url_for('article.web_article_index'))

    return render_template('articles/edit.html', article=article_serializer(article))

# HAPUS ARTIKEL
@article_bp.route('/web/articles/delete/<id>', methods=['POST'])
def web_article_delete(id):
    current_app.mongo.db.articles.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('article.web_article_index'))