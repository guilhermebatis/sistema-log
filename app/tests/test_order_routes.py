from app.models import OrderItem
from app.models.client import Client
from app.models.order_service import OrderService, OrderStatus
from app import db


def test_order_service_routes(order_service):
    response = order_service.get('orders/')
    assert response.status_code == 200


def test_order_service_create_routes(order_service):
    with order_service.application.app_context():

        client = Client(
            name = 'client_test1',
            CPF_CNPJ = '123456789',
            email = 'test1@gmail.com',
            phone = '789456123',
        )

        db.session.add(client)
        db.session.flush()

        order_service_data = {
            'client_id': client.id,
            'weight_total': 100,
            'cubage_total': 100,
            'origin': 'SP',
            'destination': 'RJ',
            'distance': 500,
            'price': 1000,
            'status': OrderStatus.PENDING.value,
        }

        response = order_service.post('/orders/create', data=order_service_data)

        order_service_exist = db.session.query(OrderService).all()

        assert response.status_code == 302
        assert len(order_service_exist) == 1


def test_order_service_update_routes(order_service):
    with order_service.application.app_context():
        client = Client(
            name='client_test1',
            CPF_CNPJ='123456789',
            email='test1@gmail.com',
            phone='789456123',
        )

        db.session.add(client)
        db.session.flush()

        order_service_data = {
            'id': 1,
            'client_id': client.id,
            'weight_total': 100,
            'cubage_total': 100,
            'origin': 'SP',
            'destination': 'RJ',
            'distance': 500,
            'price': 1000,
            'status': OrderStatus.PENDING.value,
        }

        order_service.post('/orders/create', data=order_service_data)

        order_service_data_2 = {
            'id': order_service_data['id'],
            'client_id': client.id,
            'weight_total': 100,
            'cubage_total': 100,
            'origin': 'SP',
            'destination': 'RJ',
            'distance': 500,
            'price': 1000,
            'status': OrderStatus.PENDING.value,
        }

        response = order_service.post(f'/orders/{order_service_data_2['id']}/update', data=order_service_data_2)

        order_service_exist = db.session.query(OrderService).all()

        assert response.status_code == 302
        assert len(order_service_exist) == 1


def test_order_service_delete_routes(order_service):
    with order_service.application.app_context():
        client = Client(
            name='client_test1',
            CPF_CNPJ='123456789',
            email='test1@gmail.com',
            phone='789456123',
        )

        db.session.add(client)
        db.session.flush()

        order_service_data = {
            'id': 1,
            'client_id': client.id,
            'weight_total': 100,
            'cubage_total': 100,
            'origin': 'SP',
            'destination': 'RJ',
            'distance': 500,
            'price': 1000,
            'status': OrderStatus.PENDING.value,
        }

        order_service.post('/orders/create', data=order_service_data)
        response = order_service.post(f'/orders/{order_service_data['id']}/delete')

        order_service_exist = db.session.query(OrderService).all()

        assert response.status_code == 302
        assert len(order_service_exist) == 0


def test_order_itens_routes(order_itens):
    with order_itens.application.app_context():
        response = order_itens.get('order_items/')
        assert response.status_code == 200


def test_order_itens_create_routes(order_itens):
    with order_itens.application.app_context():
        client = Client(
            name='client_test1',
            CPF_CNPJ='123456789',
            email='test1@gmail.com',
            phone='789456123',
        )

        db.session.add(client)
        db.session.flush()

        order_service = OrderService(
            id = 1,
            client_id = client.id,
            weight_total = 10,
            cubage_total = 10,
            origin = 'SP',
            destination = 'RJ',
            distance = 500,
            price = 10,
            status = OrderStatus.PENDING,
        )


        db.session.add(order_service)
        db.session.flush()


        order_itens_data = {
            'id': 1,
            'order_service_id': order_service.id,
            'quantity': 10,
            'weight': 10,
            'cubage': 10,
            'price_item': 10,
        }

        response = order_itens.post('order_items/create', data=order_itens_data)
        order_itens_exist = db.session.query(OrderItem).all()

        assert response.status_code == 302
        assert len(order_itens_exist) == 1


def test_order_itens_update_routes(order_itens):
    with order_itens.application.app_context():
        client = Client(
            name='client_test1',
            CPF_CNPJ='123456789',
            email='test1@gmail.com',
            phone='789456123',
        )

        db.session.add(client)
        db.session.flush()

        order_service = OrderService(
            id = 1,
            client_id = client.id,
            weight_total = 10,
            cubage_total = 10,
            origin = 'SP',
            destination = 'RJ',
            distance = 500,
            price = 10,
            status = OrderStatus.PENDING,
        )

        db.session.add(order_service)
        db.session.flush()

        order_itens_data = {
            'id': 1,
            'order_service_id': order_service.id,
            'quantity': 5,
            'weight': 5,
            'cubage': 5,
            'price_item': 5,
        }

        order_itens.post('order_items/create', data=order_itens_data)

        order_itens_data_up = {
            'id': 1,
            'order_service_id': order_service.id,
            'quantity': 10,
            'weight': 10,
            'cubage': 10,
            'price_item': 10,
        }

        response = order_itens.post(f'order_items/{order_itens_data_up['id']}/update', data=order_itens_data_up)
        order_itens_exist = db.session.query(OrderItem).all()

        assert response.status_code == 302
        assert len(order_itens_exist) == 1


def test_order_itens_delete_routes(order_itens):
    with order_itens.application.app_context():
        client = Client(
            name='client_test1',
            CPF_CNPJ='123456789',
            email='test1@gmail.com',
            phone='789456123',
        )

        db.session.add(client)
        db.session.flush()

        order_service = OrderService(
            id = 1,
            client_id = client.id,
            weight_total = 10,
            cubage_total = 10,
            origin = 'SP',
            destination = 'RJ',
            distance = 500,
            price = 10,
            status = OrderStatus.PENDING,
        )


        db.session.add(order_service)
        db.session.flush()


        order_itens_data = {
            'id': 1,
            'order_service_id': order_service.id,
            'quantity': 10,
            'weight': 10,
            'cubage': 10,
            'price_item': 10,
        }

        order_itens.post('order_items/create', data=order_itens_data)

        response = order_itens.post(f'/order_items/{order_itens_data['id']}/delete')
        order_itens_exist = db.session.query(OrderItem).all()

        assert response.status_code == 302
        assert len(order_itens_exist) == 0