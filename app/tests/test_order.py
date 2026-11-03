from app.models import Client
from service.order_layer import (create_order_service, update_order_item,
                                 create_order_item, delete_order_item,
                                 update_order_service, delete_order_service)
from app.models.order_service import OrderService, OrderItem
from app import db
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError
from flask import get_flashed_messages


# Test Order Service
def test_create_ordem_service(app):
    with app.test_request_context():

        client = Client(
        name = 'test',
        CPF_CNPJ = '12345',
        email = 'test@gmail.com',
        phone = '1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
        client_id = client.id,
        weight_total = 10,
        cubage_total = 10,
        origin = 'SP',
        destination = 'RJ',
        distance = 500,
        price = 1200,
        )

        result = create_order_service(order)
        assert result is True


def test_update_order_service(app):
    with app.test_request_context():
        client = Client(
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            client_id=client.id,
            weight_total=10,
            cubage_total=10,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1200,
        )

        db.session.add(order)
        db.session.commit()

        var_update_order_service = OrderService(
            id=order.id,
            client_id=client.id,
            weight_total=20,
            cubage_total=20,
            origin='RJ',
            destination='SP',
            distance=700,
            price=1500,
        )

        result = update_order_service(var_update_order_service)

        assert result is True


def test_delete_order_service(app):
    with app.test_request_context():
        client = Client(
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            client_id=client.id,
            weight_total=10,
            cubage_total=10,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1200,
        )

        db.session.add(order)
        db.session.commit()

        result = delete_order_service(order)
        assert result is True


def test_weight_negative_order_service(app):
    with app.test_request_context():
        client = Client(
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            client_id=client.id,
            weight_total=-10,
            cubage_total=10,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1200,
        )

        result = create_order_service(order)
        assert result is False


def test_cubage_negative_order_service(app):
    with app.test_request_context():
        client = Client(
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            client_id=client.id,
            weight_total=10,
            cubage_total=-10,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1200,
        )


        result = create_order_service(order)
        assert result is False


def test_origin_none_order_service(app):
    with app.test_request_context():
        client = Client(
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            client_id=client.id,
            weight_total=10,
            cubage_total=10,
            origin=None,
            destination='RJ',
            distance=500,
            price=1200,
        )

        result = create_order_service(order)
        assert result is False


def test_destination_none_order_service(app):
    with app.test_request_context():
        client = Client(
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            client_id=client.id,
            weight_total=10,
            cubage_total=10,
            origin='SP',
            destination=None,
            distance=500,
            price=1200,
        )

        result = create_order_service(order)
        assert result is False


def test_distance_negative_order_service(app):
    with app.test_request_context():
        client = Client(
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            client_id=client.id,
            weight_total=10,
            cubage_total=10,
            origin='SP',
            destination='RJ',
            distance=-500,
            price=1200,
        )

        result = create_order_service(order)
        assert result is False


def test_price_negative_order_service(app):
    with app.test_request_context():
        client = Client(
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            client_id=client.id,
            weight_total=10,
            cubage_total=10,
            origin='SP',
            destination='RJ',
            distance=500,
            price=-1200,
        )

        result = create_order_service(order)
        assert result is False


def test_distance_none_order_service(app):
    with app.test_request_context():
        client = Client(
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            client_id=client.id,
            weight_total=10,
            cubage_total=10,
            origin='SP',
            destination='RJ',
            distance=None,
            price=-1200,
        )

        result = create_order_service(order)
        assert result is False


def test_read_order_service(app):
    with app.test_request_context():
        client = Client(
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            client_id=client.id,
            weight_total=10,
            cubage_total=10,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1200,
        )

        result = create_order_service(order)
        assert result is True

        id = order.id
        order_service = db.session.get(OrderService, id)

        assert order_service.id == order.id


# Test Ordem Item
def test_create_ordem_item(app):
    with app.test_request_context():
        client = Client(
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            client_id=client.id,
            weight_total=10,
            cubage_total=10,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1200,
        )

        db.session.add(order)
        db.session.commit()

        order_item = OrderItem(
        order_service_id = order.id,
        quantity = 10,
        weight = 10,
        cubage = 10,
        price_item = 10,
        )

        result = create_order_item(order_item)
        assert result is True


def test_update_order_item(app):
    with app.test_request_context():
        client = Client(
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            client_id=client.id,
            weight_total=20,
            cubage_total=20,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1200,
        )

        db.session.add(order)
        db.session.commit()

        order_item = OrderItem(
            id=1,
            order_service_id = order.id,
            quantity = 10,
            weight = 10,
            cubage = 10,
            price_item = 10,
        )

        db.session.add(order_item)
        db.session.commit()

        var_update_order_item = OrderItem(
            id=order_item.id,
            order_service_id = order.id,
            quantity = 20,
            weight = 20,
            cubage = 20,
            price_item = 20,
        )

        result = update_order_item(var_update_order_item)
        assert result is True


def test_delete_order_item(app):
    with app.test_request_context():
        client = Client(
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            id=1,
            client_id=client.id,
            weight_total=20,
            cubage_total=20,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1200,
        )

        db.session.add(order)
        db.session.commit()

        order_item = OrderItem(
            id=1,
            order_service_id=order.id,
            quantity=10,
            weight=10,
            cubage=10,
            price_item=10,
        )

        db.session.add(order_item)
        db.session.commit()

        result = delete_order_item(order_item)
        assert result is True


def test_order_service_id_none_ordem_item(app):
    with app.test_request_context():
        client = Client(
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            id = 1,
            client_id=client.id,
            weight_total=10,
            cubage_total=10,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1200,
        )

        db.session.add(order)
        db.session.commit()

        order_item = OrderItem(
        order_service_id = None,
        quantity = 10,
        weight = 10,
        cubage = 10,
        price_item = 10,
        )

        result = create_order_item(order_item)
        assert result is False


def test_order_quantity_none_ordem_item(app):
    with app.test_request_context():
        client = Client(
            id=1,
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            id = 1,
            client_id=1,
            weight_total=10,
            cubage_total=10,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1200,
        )

        db.session.add(order)
        db.session.commit()

        order_item = OrderItem(
        order_service_id = 1,
        quantity = None,
        weight = 10,
        cubage = 10,
        price_item = 10,
        )

        result = create_order_item(order_item)
        assert result is False


def test_order_weight_none_ordem_item(app):
    with app.test_request_context():
        client = Client(
            id=1,
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            id = 1,
            client_id=1,
            weight_total=10,
            cubage_total=10,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1200,
        )

        db.session.add(order)
        db.session.commit()

        order_item = OrderItem(
        order_service_id = 1,
        quantity = 10,
        weight = None,
        cubage = 10,
        price_item = 10,
        )

        result = create_order_item(order_item)
        assert result is False


def test_order_cubage_none_ordem_item(app):
    with app.test_request_context():
        client = Client(
            id=1,
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            id = 1,
            client_id=1,
            weight_total=10,
            cubage_total=10,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1200,
        )

        db.session.add(order)
        db.session.commit()

        order_item = OrderItem(
        order_service_id = 1,
        quantity = 10,
        weight = 10,
        cubage = None,
        price_item = 10,
        )

        result = create_order_item(order_item)
        assert result is False


def test_order_price_item_none_ordem_item(app):
    with app.test_request_context():
        client = Client(
            id=1,
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            id = 1,
            client_id=1,
            weight_total=10,
            cubage_total=10,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1200,
        )

        db.session.add(order)
        db.session.commit()

        order_item = OrderItem(
        order_service_id = 1,
        quantity = 10,
        weight = 10,
        cubage = 10,
        price_item = None,
        )

        result = create_order_item(order_item)
        assert result is False


def test_order_quantity_negative_ordem_item(app):
    with app.test_request_context():
        client = Client(
            id=1,
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            id = 1,
            client_id=1,
            weight_total=10,
            cubage_total=10,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1200,
        )

        db.session.add(order)
        db.session.commit()

        order_item = OrderItem(
        order_service_id = 1,
        quantity = -10,
        weight = 10,
        cubage = 10,
        price_item = 10,
        )

        result = create_order_item(order_item)
        assert result is False


def test_order_weight_negative_ordem_item(app):
    with app.test_request_context():
        client = Client(
            id=1,
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            id = 1,
            client_id=1,
            weight_total=10,
            cubage_total=10,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1200,
        )

        db.session.add(order)
        db.session.commit()

        order_item = OrderItem(
        order_service_id = 1,
        quantity = 10,
        weight = -10,
        cubage = 10,
        price_item = 10,
        )

        result = create_order_item(order_item)
        assert result is False


def test_order_cubage_negative_ordem_item(app):
    with app.test_request_context():
        client = Client(
            id=1,
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            id = 1,
            client_id=1,
            weight_total=10,
            cubage_total=10,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1200,
        )

        db.session.add(order)
        db.session.commit()

        order_item = OrderItem(
        order_service_id = 1,
        quantity = 10,
        weight = 10,
        cubage = -10,
        price_item = 10,
        )

        result = create_order_item(order_item)
        assert result is False


def test_order_price_item_negative_ordem_item(app):
    with app.test_request_context():
        client = Client(
            id=1,
            name='test',
            CPF_CNPJ='12345',
            email='test@gmail.com',
            phone='1233456',
        )

        db.session.add(client)
        db.session.commit()

        order = OrderService(
            id = 1,
            client_id=1,
            weight_total=10,
            cubage_total=10,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1200,
        )

        db.session.add(order)
        db.session.commit()

        order_item = OrderItem(
        order_service_id = 1,
        quantity = 10,
        weight = 10,
        cubage = 10,
        price_item = -10,
        )

        result = create_order_item(order_item)
        assert result is False
