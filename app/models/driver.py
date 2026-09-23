from app.extensions import db
from enum import Enum


class DriverStatus(Enum):
    AVAILABLE = "AVAILABLE"
    IN_ROUTE = "IN_ROUTE"
    UNAVAILABLE = "UNAVAILABLE"


class DrivingLicenceCategory(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cnh = db.Column(db.String(40), nullable=False, unique=True)
    phone = db.Column(db.String(100), nullable=False)
    admission_date = db.Column(db.Date)
    licence_category = db.Column(
        db.Enum(DrivingLicenceCategory, name="driving_licence_category"),
        nullable=False,)
    license_expiration_date = db.Column(db.Date)
    status = db.Column(db.Enum(DriverStatus, name="driver_status"),
                       nullable=False,
                       default=DriverStatus.AVAILABLE)

    deliveries = db.relationship("Delivery", back_populates="driver")
