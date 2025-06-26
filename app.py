from flask import Flask
from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from config import Config
from routes.auth_routes import auth_bp
from routes.google_oauth import google_auth_bp
from routes.article_routes import article_bp
from routes.gallery_routes import gallery_bp
from routes.favorite_routes import favorite_bp
from routes.user_routes import user_bp
from routes.video_routes import video_bp
from routes.batik_place_routes import batik_place_bp

app = Flask(__name__)
app.config.from_object(Config)

# Inisialisasi extension
mongo = PyMongo(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

# Bikin bisa diakses dari current_app
app.mongo = mongo
app.jwt = jwt
app.bcrypt = bcrypt
app.mail = mail

# Register blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(google_auth_bp)
app.register_blueprint(article_bp)
app.register_blueprint(user_bp)
app.register_blueprint(gallery_bp)
app.register_blueprint(favorite_bp)
app.register_blueprint(video_bp)
app.register_blueprint(batik_place_bp)


if __name__ == '__main__':
    app.run(debug=True)
