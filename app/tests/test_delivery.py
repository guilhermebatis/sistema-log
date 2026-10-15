from service.delivery_layer import create_delivery_item
from app.models.delivery import Delivery, DeliveryItem, StatusDelivery
from app.models.order_service import OrderService, OrderItem
from app import db
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError


def test_create_delivery_item(app):
    with app.test_request_context():

        order_service = OrderService(
        weight_total = 10.0,
        cubage_total = 10.0,
        origin = 'SP',
        destination = 'RJ',
        distance = 500.0,
        price = 5000.0,
        )

        db.session.add(order_service)
        db.session.flush()
        id_ordem_service = order_service.id

        delivery = Delivery(
        order_service_id=id_ordem_service,
        )

        db.session.add(delivery)
        db.session.flush()
        id_delivery = delivery.id

        ordem_item = OrderItem(
        order_service_id = id_ordem_service,
        weight = 10.0,
        cubage = 10.0,
        quantity = 10,
        price_item = 2.0,
        )

        db.session.add(ordem_item)
        db.session.flush()
        id_ordem_item = ordem_item.id

        delivery_item = DeliveryItem(
        order_item_id = id_ordem_item,
        delivery_id = id_delivery,
        weight = 10,
        cubage = 10,
        quantity = 10,)

        result = create_delivery_item(delivery_item)
        assert result is True


def test_create_delivery_item_quantity(app):
    delivery_item = DeliveryItem(
        order_item_id=1,
        delivery_id=1,
        weight=10,
        cubage=10,
        quantity=0)

    with app.test_request_context():
        result = create_delivery_item(delivery_item)
    assert result is False


def test_create_delivery_item_nonegative(app):
    delivery_item = DeliveryItem(
        order_item_id=1,
        delivery_id=1,
        weight=10,
        cubage=10,
        quantity=-10)

    with app.test_request_context():
        result = create_delivery_item(delivery_item)
    assert result is False


def test_create_delivery_item_cubage_nonegative(app):
    delivery_item = DeliveryItem(
        order_item_id=1,
        delivery_id=1,
        weight=10,
        cubage=-10,
        quantity=10)

    with app.test_request_context():
        result = create_delivery_item(delivery_item)
    assert result is False


def test_create_delivery_item_weight_nonegative(app):
    delivery_item = DeliveryItem(
        order_item_id=1,
        delivery_id=1,
        weight=-10,
        cubage=10,
        quantity=10)

    with app.test_request_context():
        result = create_delivery_item(delivery_item)
    assert result is False


def test_create_delivery_item_maximum_quantity_delivery(app):
    with app.test_request_context():

        order_service = OrderService(
        weight_total = 10.0,
        cubage_total = 10.0,
        origin = 'SP',
        destination = 'RJ',
        distance = 500.0,
        price = 5000.0,
        )

        db.session.add(order_service)
        db.session.flush()
        id_ordem_service = order_service.id

        delivery = Delivery(
        order_service_id=id_ordem_service,
        )

        db.session.add(delivery)
        db.session.flush()
        id_delivery = delivery.id

        ordem_item = OrderItem(
        order_service_id = id_ordem_service,
        weight = 10.0,
        cubage = 10.0,
        quantity = 10,
        price_item = 2.0,
        )

        db.session.add(ordem_item)
        db.session.flush()
        id_ordem_item = ordem_item.id

        delivery_item = DeliveryItem(
            order_item_id=id_ordem_item,
            delivery_id=id_delivery,
            weight=10,
            cubage=10,
            quantity=10, )

        delivery_item_2 = DeliveryItem(
        order_item_id = id_ordem_item,
        delivery_id = id_delivery,
        weight = 10,
        cubage = 10,
        quantity = 1,)

        result = create_delivery_item(delivery_item)
        assert result is True
        result = create_delivery_item(delivery_item_2)
        assert result is False


def test_create_delivery_item_no_order_item(app):
    with app.test_request_context():
        order_service = OrderService(
            weight_total=10.0,
            cubage_total=10.0,
            origin='SP',
            destination='RJ',
            distance=500.0,
            price=5000.0,
        )

        db.session.add(order_service)
        db.session.flush()
        id_ordem_service = order_service.id

        delivery = Delivery(
            order_service_id=id_ordem_service,
        )

        db.session.add(delivery)
        db.session.flush()
        id_delivery = delivery.id


        delivery_item = DeliveryItem(
            order_item_id=123,
            delivery_id=id_delivery,
            weight=10,
            cubage=10,
            quantity=10, )

        result = create_delivery_item(delivery_item)
        assert result is False


def test_create_delivery_item_no_delivery(app):
    with app.test_request_context():
        order_service = OrderService(
            weight_total=10.0,
            cubage_total=10.0,
            origin='SP',
            destination='RJ',
            distance=500.0,
            price=5000.0,
        )

        db.session.add(order_service)
        db.session.flush()
        id_ordem_service = order_service.id

        ordem_item = OrderItem(
            order_service_id=id_ordem_service,
            weight=10.0,
            cubage=10.0,
            quantity=10,
            price_item=2.0,
        )

        db.session.add(ordem_item)
        db.session.flush()
        id_ordem_item = ordem_item.id

        delivery_item = DeliveryItem(
            order_item_id=id_ordem_item,
            delivery_id=123,
            weight=10,
            cubage=10,
            quantity=10, )

        result = create_delivery_item(delivery_item)
        assert result is False


def test_create_delivery_item_delivery_no_status(app):
    with app.test_request_context():
        order_service = OrderService(
            weight_total=10.0,
            cubage_total=10.0,
            origin='SP',
            destination='RJ',
            distance=500.0,
            price=5000.0,
        )

        db.session.add(order_service)
        db.session.flush()
        id_ordem_service = order_service.id

        delivery = Delivery(
            order_service_id=id_ordem_service,
            status = StatusDelivery.CANCELLED,
        )

        db.session.add(delivery)
        db.session.flush()
        id_delivery = delivery.id

        ordem_item = OrderItem(
            order_service_id=id_ordem_service,
            weight=10.0,
            cubage=10.0,
            quantity=10,
            price_item=2.0,
        )

        db.session.add(ordem_item)
        db.session.flush()
        id_ordem_item = ordem_item.id

        delivery_item = DeliveryItem(
            order_item_id=id_ordem_item,
            delivery_id=id_delivery,
            weight=10,
            cubage=10,
            quantity=10, )

        result = create_delivery_item(delivery_item)
        assert result is False


def test_create_delivery_item_order_service_different(app):
    with app.test_request_context():
        order_service_1 = OrderService(
            weight_total=10.0,
            cubage_total=10.0,
            origin='SP',
            destination='RJ',
            distance=500.0,
            price=5000.0,
        )

        order_service_2 = OrderService(
            weight_total=10.0,
            cubage_total=10.0,
            origin='SP',
            destination='RJ',
            distance=500.0,
            price=5000.0,
        )

        db.session.add(order_service_1)
        db.session.add(order_service_2)
        db.session.flush()
        id_ordem_service_1 = order_service_1.id
        id_ordem_service_2 = order_service_2.id

        delivery = Delivery(
            order_service_id=id_ordem_service_1,
        )

        db.session.add(delivery)
        db.session.flush()
        id_delivery = delivery.id

        ordem_item = OrderItem(
            order_service_id=id_ordem_service_2,
            weight=10.0,
            cubage=10.0,
            quantity=10,
            price_item=2.0,
        )

        db.session.add(ordem_item)
        db.session.flush()
        id_ordem_item = ordem_item.id

        delivery_item = DeliveryItem(
            order_item_id=id_ordem_item,
            delivery_id=id_delivery,
            weight=10,
            cubage=10,
            quantity=10, )

        result = create_delivery_item(delivery_item)
        assert result is False


def test_create_delivery_item_integrity_error(app):
    with app.test_request_context():

        order_service = OrderService(
        weight_total = 10.0,
        cubage_total = 10.0,
        origin = 'SP',
        destination = 'RJ',
        distance = 500.0,
        price = 5000.0,
        )

        db.session.add(order_service)
        db.session.flush()
        id_ordem_service = order_service.id

        delivery = Delivery(
        order_service_id=id_ordem_service,
        )

        db.session.add(delivery)
        db.session.flush()
        id_delivery = delivery.id

        ordem_item = OrderItem(
        order_service_id = id_ordem_service,
        weight = 10.0,
        cubage = 10.0,
        quantity = 10,
        price_item = 2.0,
        )

        db.session.add(ordem_item)
        db.session.flush()
        id_ordem_item = ordem_item.id

        delivery_item = DeliveryItem(
        order_item_id = id_ordem_item,
        delivery_id = id_delivery,
        weight = 10,
        cubage = 10,
        quantity = 10,)

        with patch(
                "service.delivery_layer.db.session.commit",
                side_effect=IntegrityError(
                    "INSERT",
                    {},
                    Exception("Erro simulado"),
                ),
        ), patch(
            "service.delivery_layer.db.session.rollback"
        ) as mock_rollback:
            result = create_delivery_item(delivery_item)

        assert result is False
        mock_rollback.assert_called_once()
