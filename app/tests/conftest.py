from app import create_app
from app.config import TestConfig
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

    return app


