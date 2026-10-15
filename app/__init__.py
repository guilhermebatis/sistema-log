from flask import Flask
from .config import Config
from .extensions import db, migrate
from sqlalchemy import text
from app.routes.health import health_bp
from app import models
from app.routes.clients import client_bp
from app.routes.vehicle import vehicle_bp
from app.routes.driver import  driver_bp
from app.routes.orders import orders_bp
from app.routes.order_items import order_items_bp
from app.routes.delivery import delivery_bp
from app.routes.delivery_itens import delivery_itens_bp

def create_app(test_config=None):
    # APP
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config is not None:
        app.config.update(test_config)

    # BD AND MIGRATIONS
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.session.execute(text("SELECT 1"))

    # BLUEPRINT
    app.register_blueprint(health_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(vehicle_bp)
    app.register_blueprint(driver_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(order_items_bp)
    app.register_blueprint(delivery_bp)
    app.register_blueprint(delivery_itens_bp)

    return app
