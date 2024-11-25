from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from app.config import Config
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
api = Api(version="1.0", title="Compound v2 API", description="API to fetch user points from Compound v2")


def create_app():
    """Application factory pattern."""
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration
    app.config.from_object(Config)

    # Print the database URI for debugging
    print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])

    # Ensure the directory for SQLite file exists (if using SQLite)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///'):
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '', 1)
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    # Register routes
    from app.routes import register_routes
    register_routes(api)

    return app
