from app import create_app, db
from app.config import TestConfig

app = create_app(
    test_config={
        "TESTING": TestConfig.TESTING,
        "SQLALCHEMY_DATABASE_URI": TestConfig.SQLALCHEMY_DATABASE_URI,
    }
)

with app.app_context():
    print("Banco conectado:", db.engine.url.database)

    with db.engine.connect() as connection:
        result = connection.exec_driver_sql(
            "SHOW COLUMNS FROM delivery_item"
        )

        print("Colunas de delivery_item:")
        for column in result:
            print(column)
