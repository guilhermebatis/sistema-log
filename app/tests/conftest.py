from app import create_app
from app.config import TestConfig
from app.extensions import db
import pytest


@pytest.fixture
def app():
    app = create_app(
        test_config={
            "TESTING": TestConfig.TESTING,
            "SQLALCHEMY_DATABASE_URI": TestConfig.SQLALCHEMY_DATABASE_URI,
        }
    )

    print("Banco de testes:", app.config["SQLALCHEMY_DATABASE_URI"])

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()
