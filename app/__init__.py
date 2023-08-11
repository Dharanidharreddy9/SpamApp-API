
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restx import Api
from config import Config

# Create instances of extensions
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
api = Api()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    api.init_app(app)

    # Import and register blueprints
    from app.view import spamfinder
    app.register_blueprint(spamfinder)

    return app
