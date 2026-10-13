from app.extensions import db
from enum import Enum
from sqlalchemy import CheckConstraint


class StatusDelivery(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"


class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_service_id = db.Column(db.Integer,
                                 db.ForeignKey("order_service.id"),
                                 nullable=False)
    status = db.Column(db.Enum(StatusDelivery, name="delivery_status"),
                       nullable=False,
                       default=StatusDelivery.PENDING)
    driver_id = db.Column(db.Integer,
                          db.ForeignKey("driver.id"),
                          )
    vehicle_id = db.Column(db.Integer,
                           db.ForeignKey("vehicle.id"),
                           )

    # ORM
    delivery_itens = db.relationship("DeliveryItem", back_populates="delivery")
    order_service = db.relationship(
        "OrderService", back_populates="deliveries")
    driver = db.relationship("Driver", back_populates="deliveries")
    vehicles = db.relationship("Vehicle", back_populates="deliveries")


class DeliveryItem(db.Model):

    __table_args__ = (
        CheckConstraint('weight >= 0',
                        name='weight_nonnegative'),
        CheckConstraint('cubage >= 0',
                        name='cubage_nonnegative'),
        CheckConstraint('quantity >= 0',
                        name='quantity_nonnegative'),
    )

    id = db.Column(db.Integer, primary_key=True)
    order_item_id = db.Column(db.Integer,
                              db.ForeignKey("order_item.id"),
                              nullable=False)
    delivery_id = db.Column(db.Integer,
                            db.ForeignKey("delivery.id"),
                            nullable=False)
    weight = db.Column(db.Numeric(10, 2), nullable=False)
    cubage = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer(10, 2), nullable=False)

    delivery = db.relationship("Delivery", back_populates="delivery_itens")
    order_item = db.relationship("OrderItem", back_populates="delivery_items")
