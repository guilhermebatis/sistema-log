from app.extensions import db
from datetime import date


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    CPF_CNPJ = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    phone = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.Date, default=date.today)

    orders = db.relationship("OrderService", back_populates="client")
