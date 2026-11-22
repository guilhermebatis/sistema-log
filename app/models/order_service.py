from app.extensions import db
from enum import Enum
from sqlalchemy import CheckConstraint
from datetime import datetime
from decimal import Decimal

class OrderStatus(Enum):
    PENDING = "PENDING"
    QUOTED = "QUOTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class OrderService(db.Model):

    __table_args__ = (
        CheckConstraint("weight_total >= 0",
                        name="ck_order_service_weight_total_nonnegative"),
        CheckConstraint('cubage_total >= 0', name="ck_order_service_cubage_total_nonnegative"),
        CheckConstraint('distance >= 0', name="ck_order_service_distance_nonnegative"),
        CheckConstraint('price >= 0', name="ck_order_service_price_nonnegative"),
    )


    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer,
                          db.ForeignKey("client.id"),
                          )
    created_at = db.Column(db.DateTime, default=datetime.now)
    weight_total = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))
    cubage_total = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))
    origin = db.Column(db.String(20), nullable=False)
    destination = db.Column(db.String(20), nullable=False)
    distance = db.Column(db.Numeric(10, 2),  nullable=False)
    price = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))
    status = db.Column(db.Enum(OrderStatus, name="order_status"),
                       nullable=False,
                       default=OrderStatus.PENDING)

    client = db.relationship("Client", back_populates="orders_service")
    order_items = db.relationship("OrderItem", back_populates="order")
    deliveries = db.relationship("Delivery", back_populates="order_service")


    def calculate_totals(self):
        weight_total = Decimal('0.00')
        cubage_total = Decimal('0.00')
        price = Decimal('0.00')
        for itens in self.order_items:
            weight_total += itens.quantity * itens.weight
            cubage_total += itens.quantity * itens.cubage
            price += itens.quantity * itens.price_item

        self.weight_total = weight_total
        self.cubage_total = cubage_total
        self.price = price


class OrderItem(db.Model):

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="ck_order_item_quantity_nonnegative"),
        CheckConstraint("weight >= 0", name="ck_order_item_weight_nonnegative"),
        CheckConstraint("cubage >= 0", name="ck_order_item_cubage_nonnegative"),
        CheckConstraint("price_item >= 0", name="ck_order_item_price_item_nonnegative"),
    )

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
    order = db.relationship("OrderService", back_populates="order_items")
    delivery_items = db.relationship(
        "DeliveryItem", back_populates="order_item")
