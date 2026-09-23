from app.extensions import db
from enum import Enum


class OrderStatus(Enum):
    PENDING = "PENDING"
    QUOTED = "QUOTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class OrderService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer,
                          db.ForeignKey("client.id"),
                          nullable=False,)
    weight_total = db.Column(db.Numeric(10, 2))
    cubage_total = db.Column(db.Numeric(10, 2))
    origin = db.Column(db.String(20), nullable=False)
    destination = db.Column(db.String(20), nullable=False)
    distance = db.Column(db.Numeric(10, 2),  nullable=False)
    price = db.Column(db.Numeric(10, 2))
    status = db.Column(db.Enum(OrderStatus, name="order_status"),
                       nullable=False,
                       default=OrderStatus.PENDING)

    client = db.relationship("Client", back_populates="orders_service")
    order_item = db.relationship("Order_item", back_populates="order")
    deliveries = db.relationship("Delivery", back_populates="order_service")


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_service_id = db.Column(db.Integer,
                                 db.ForeignKey("order_service.id"),
                                 nullable=False,)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100))
    weight = db.Column(db.Numeric(10, 2), nullable=False)
    cubage = db.Column(db.Numeric(10, 2), nullable=False)
    price_item = db.Column(db.Numeric(10, 2), nullable=False)

    # ORM
    order = db.relationship("OrderService", back_populates="order_item")
    delivery_items = db.relationship(
        "DeliveryItem", back_populates="order_item")
