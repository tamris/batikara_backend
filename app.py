from flask import Flask
from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import Config
from routes.auth_web import auth_web_bp
from routes.auth_routes import auth_bp
from routes.google_oauth import google_auth_bp
from routes.article_routes import article_bp
from routes.gallery_routes import gallery_bp
from routes.favorite_routes import favorite_bp
from routes.user_routes import user_bp
from routes.dashboard_routes import dashboard_bp
from routes.event_routes import event_bp
from routes.video_routes import video_bp
from routes.batik_place_routes import batik_place_bp
from routes.reset_password_routes import reset_bp
from routes.predict_route import predict_bp 

app = Flask(__name__)
CORS(app)
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
app.register_blueprint(auth_web_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(google_auth_bp)
app.register_blueprint(article_bp)
app.register_blueprint(user_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(gallery_bp)
app.register_blueprint(favorite_bp)
app.register_blueprint(video_bp)
app.register_blueprint(event_bp)
app.register_blueprint(batik_place_bp)
app.register_blueprint(reset_bp)
app.register_blueprint(predict_bp)

if __name__ == '__main__':
    app.run(debug=True)
