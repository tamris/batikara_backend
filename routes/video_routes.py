from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from bson import ObjectId
from models import video_model

video_bp = Blueprint('video_bp', __name__, url_prefix='/videos')

@video_bp.route('/')
def index():
    videos = video_model.get_all_videos()
    for v in videos:
        v['_id'] = str(v['_id'])
    return render_template('videos/index.html', videos=videos)

@video_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'youtubeUrl': request.form['youtubeUrl']
        }
        video_model.insert_video(data)
        return redirect(url_for('video_bp.index'))
    return render_template('videos/create.html')

@video_bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    video = video_model.get_video_by_id(ObjectId(id))
    if request.method == 'POST':
        data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'youtubeUrl': request.form['youtubeUrl']
        }
        video_model.update_video(ObjectId(id), data)
        return redirect(url_for('video_bp.index'))
    video['_id'] = str(video['_id'])
    return render_template('videos/edit.html', video=video)

@video_bp.route('/delete/<id>')
def delete(id):
    video_model.delete_video(ObjectId(id))
    return redirect(url_for('video_bp.index'))

# Endpoint untuk Flutter: GET all video
@video_bp.route('/api', methods=['GET'])
def api_get_videos():
    videos = video_model.get_all_videos()
    for video in videos:
        video['_id'] = str(video['_id'])
    return jsonify(videos)
