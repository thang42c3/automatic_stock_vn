from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import Config

db = SQLAlchemy()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.app_context()
    app.config.from_object(config_class)
    db.init_app(app)

    from app.main.controller import bp as main_bp
    app.register_blueprint(main_bp)
    return app

