from flask import Flask
from .config import Config
from .extensions import db, migrate
from sqlalchemy import text
from app.routes.health import health_bp


def create_app():
    # APP
    app = Flask(__name__)
    app.config.from_object(Config)

    # BD AND MIGRATIONS
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.session.execute(text("SELECT 1"))

    # BLUEPRINT
    app.register_blueprint(health_bp)

    return app
