from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os
from flask_cors import CORS


# Initialize SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    # CORS(app)
    CORS(app, resources={r"/api/*": {"origins": "http://sheltrnow-frontend.s3-website.us-east-2.amazonaws.com"}})


    load_dotenv()

    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from .routes.user_routes import user_bp
    from .routes.flood_alerts_routes import flood_alert_bp
    from .routes.shelter_routes import shelter_bp
    from .routes.chat_bot_routes import chat_bot_bp

    app.register_blueprint(flood_alert_bp, url_prefix='/api/alerts')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(shelter_bp, url_prefix='/api/shelters')
    app.register_blueprint(chat_bot_bp, url_prefix='/api/chatbot')

    return app
