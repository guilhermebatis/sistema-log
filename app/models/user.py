from datetime import datetime, timezone
from flask_login import UserMixin
from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean(), default=True, nullable=False)
    role = db.Column(db.String(64), default='user', nullable=False)
    created_at = db.Column(db.DateTime(),
                           nullable=False,
                           default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))