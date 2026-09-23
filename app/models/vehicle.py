from app.extensions import db
from sqlalchemy import CheckConstraint
from enum import Enum


class VehicleStatus(Enum):
    AVAILABLE = "AVAILABLE"
    MAINTENANCE = "MAINTENANCE"
    UNAVAILABLE = "UNAVAILABLE"


class FuelType(Enum):
    DIESEL = "DIESEL"
    GASOLINE = "GASOLINE"
    ETHANOL = "ETHANOL"
    FLEX = "FLEX"
    ELECTRIC = "ELECTRIC"


class Vehicle(db.Model):

    __table_args__ = (
        CheckConstraint("cargo_capacity_kg > 0",
                        name="ck_vehicle_capacity_kg_positive"),
        CheckConstraint("cargo_capacity_m3 > 0",
                        name="ck_vehicle_capacity_m_positive"),
        CheckConstraint("axle_count > 0",
                        name="ck_vehicle_axle_count_positive"),
        CheckConstraint("odometer >= 0",
                        name="ck_vehicle_odometer_nonnegative"),
    )

    id = db.Column(db.Integer, primary_key=True)
    cargo_capacity_kg = db.Column(db.Integer, nullable=False)
    cargo_capacity_m3 = db.Column(db.Numeric(10, 2), nullable=False)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.Enum(VehicleStatus, name="vehicle_status"),
                       nullable=False,
                       default=VehicleStatus.AVAILABLE)
    model = db.Column(db.String(100), nullable=False)
    axle_count = db.Column(db.Integer, nullable=False)
    odometer = db.Column(db.Integer, nullable=False)
    fuel_type = db.Column(db.Enum(FuelType, name="vehicle_fuel_type"),
                          nullable=False)

    deliveries = db.relationship("Delivery", back_populates="vehicles")
