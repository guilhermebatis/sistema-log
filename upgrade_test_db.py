from flask_migrate import upgrade
from app import create_app
from app.config import TestConfig

app = create_app(
    test_config={
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TestConfig.SQLALCHEMY_DATABASE_URI,
    }
)

with app.app_context():
    print("Banco selecionado:", app.config["SQLALCHEMY_DATABASE_URI"].database)
    upgrade()
    print("Migrations aplicadas!")
