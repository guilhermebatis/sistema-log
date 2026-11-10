from app.models import Delivery, OrderService, Vehicle, Driver, Client
from app import db
import datetime
from app.models.driver import DrivingLicenceCategory, DriverStatus
from app.models.vehicle import FuelType, VehicleStatus
from app.models.order_service import OrderStatus, OrderItem
from app.models.delivery import Delivery, DeliveryItem
from flask import get_flashed_messages


def test_delivery_routes(delivery):
    response = delivery.get('delivery/')
    assert response.status_code == 200


def test_delivery_route_create_delivery(delivery):
    with delivery.application.app_context():
        client = Client(
            name = 'client_test1',
            CPF_CNPJ = '123456789',
            email = 'test1@gmail.com',
            phone = '789456123',
        )

        db.session.add(client)
        db.session.flush()

        order_service = OrderService(
            client_id=client.id,
            weight_total = 100,
            cubage_total = 100,
            origin = 'SP',
            destination = 'RJ',
            distance = 500,
            price = 1000,
            status = OrderStatus.PENDING,
        )

        driver = Driver(
            name= 'driver_test1',
            cnh = '123456789',
            phone = '987654321',
            admission_date = datetime.datetime.now(),
            licence_category = DrivingLicenceCategory.E,
            license_expiration_date = datetime.datetime.now(),
            status = DriverStatus.AVAILABLE
        )

        vehicle = Vehicle(
            cargo_capacity_kg = 1000,
            cargo_capacity_m3 = 1000,
            license_plate = 'TXQ-8451',
            model = 'MERCEDES',
            status = VehicleStatus.AVAILABLE,
            axle_count = 6,
            odometer = 20000,
            fuel_type = FuelType.DIESEL,
        )

        db.session.add_all([
            order_service,
            driver,
            vehicle
        ])

        db.session.flush()

        data_delivery = {
        'order_service_id':  order_service.id,
        'driver_id':  driver.id,
        'vehicle_id':  vehicle.id,
        }

        response = delivery.post('/delivery/create', data=data_delivery)

        delivery_created = db.session.query(Delivery).all()
        assert response.status_code == 302
        assert len(delivery_created) == 1


def test_delivery_route_update_delivery(delivery):
    with delivery.application.app_context():
        client = Client(
            name='client_test1',
            CPF_CNPJ='123456789',
            email='test1@gmail.com',
            phone='789456123',
        )

        db.session.add(client)
        db.session.flush()

        order_service = OrderService(
            client_id=client.id,
            weight_total=100,
            cubage_total=100,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1000,
            status=OrderStatus.PENDING,
        )

        driver = Driver(
            name='driver_test1',
            cnh='123456789',
            phone='987654321',
            admission_date=datetime.datetime.now(),
            licence_category=DrivingLicenceCategory.E,
            license_expiration_date=datetime.datetime.now(),
            status=DriverStatus.AVAILABLE
        )

        vehicle = Vehicle(
            cargo_capacity_kg=1000,
            cargo_capacity_m3=1000,
            license_plate='TXQ-8451',
            model='MERCEDES',
            status=VehicleStatus.AVAILABLE,
            axle_count=6,
            odometer=20000,
            fuel_type=FuelType.DIESEL,
        )

        vehicle_2 = Vehicle(
            cargo_capacity_kg=1000,
            cargo_capacity_m3=1000,
            license_plate='TYX-9696',
            model='MERCEDES',
            status=VehicleStatus.AVAILABLE,
            axle_count=6,
            odometer=20000,
            fuel_type=FuelType.DIESEL,
        )

        db.session.add_all([
            order_service,
            driver,
            vehicle,
            vehicle_2,
        ])

        db.session.flush()

        data_delivery = {
            'order_service_id': order_service.id,
            'driver_id': driver.id,
            'vehicle_id': vehicle.id,
        }

        data_delivery_2 = {
            'order_service_id': order_service.id,
            'driver_id': driver.id,
            'vehicle_id': vehicle_2.id,
        }

        delivery.post('/delivery/create', data=data_delivery)

        exist_delivery = db.session.get(Delivery, 1)

        response = delivery.post(f'/delivery/{exist_delivery.id}/update', data=data_delivery_2)

        delivery_created = db.session.query(Delivery).all()
        assert response.status_code == 302
        assert len(delivery_created) == 1
        assert exist_delivery.vehicles.license_plate == 'TYX-9696'


def test_delivery_route_delete_delivery(delivery):
    with delivery.application.app_context():
        client = Client(
            name = 'client_test1',
            CPF_CNPJ = '123456789',
            email = 'test1@gmail.com',
            phone = '789456123',
        )

        db.session.add(client)
        db.session.flush()

        order_service = OrderService(
            client_id=client.id,
            weight_total = 100,
            cubage_total = 100,
            origin = 'SP',
            destination = 'RJ',
            distance = 500,
            price = 1000,
            status = OrderStatus.PENDING,
        )

        driver = Driver(
            name= 'driver_test1',
            cnh = '123456789',
            phone = '987654321',
            admission_date = datetime.datetime.now(),
            licence_category = DrivingLicenceCategory.E,
            license_expiration_date = datetime.datetime.now(),
            status = DriverStatus.AVAILABLE
        )

        vehicle = Vehicle(
            cargo_capacity_kg = 1000,
            cargo_capacity_m3 = 1000,
            license_plate = 'TXQ-8451',
            model = 'MERCEDES',
            status = VehicleStatus.AVAILABLE,
            axle_count = 6,
            odometer = 20000,
            fuel_type = FuelType.DIESEL,
        )

        db.session.add_all([
            order_service,
            driver,
            vehicle
        ])

        db.session.flush()

        data_delivery = {
        'order_service_id':  order_service.id,
        'driver_id':  driver.id,
        'vehicle_id':  vehicle.id,
        }

        delivery.post('/delivery/create', data=data_delivery)

        response = delivery.post(f'/delivery/1/delete')

        delivery_created = db.session.query(Delivery).all()
        assert response.status_code == 302
        assert len(delivery_created) == 0


def test_delivery_itens_route(delivery_itens):
    with delivery_itens.application.app_context():
        response = delivery_itens.get('delivery_itens/')
        assert response.status_code == 200


def test_delivery_itens_create_route(delivery_itens):
    with delivery_itens.application.app_context():
        client = Client(
            name = 'client_test1',
            CPF_CNPJ = '123456789',
            email = 'test1@gmail.com',
            phone = '789456123',
        )

        db.session.add(client)
        db.session.flush()

        order_service = OrderService(
            client_id=client.id,
            weight_total=100,
            cubage_total=100,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1000,
            status=OrderStatus.PENDING,
        )

        db.session.add(order_service)
        db.session.flush()

        order_item = OrderItem(
            order_service_id=order_service.id,
            quantity = 10,
            weight = 10.0,
            cubage = 10.0,
            price_item = 100,
        )

        driver = Driver(
            name='driver_test1',
            cnh='123456789',
            phone='987654321',
            admission_date=datetime.datetime.now(),
            licence_category=DrivingLicenceCategory.E,
            license_expiration_date=datetime.datetime.now(),
            status=DriverStatus.AVAILABLE
        )

        vehicle = Vehicle(
            cargo_capacity_kg=1000,
            cargo_capacity_m3=1000,
            license_plate='TXQ-8451',
            model='MERCEDES',
            status=VehicleStatus.AVAILABLE,
            axle_count=6,
            odometer=20000,
            fuel_type=FuelType.DIESEL,
        )

        db.session.add_all([
            order_item,
            driver,
            vehicle
        ])

        db.session.flush()

        delivery = Delivery(
            order_service_id = order_service.id,
            driver_id = driver.id,
            vehicle_id =  vehicle.id,
        )

        db.session.add(delivery)
        db.session.flush()

        delivery_itens_data = {
            'order_item_id': order_item.id,
            'delivery_id': delivery.id,
            'weight': 10.0,
            'cubage': 10.0,
            'quantity': 10,
        }

        response = delivery_itens.post('/delivery_itens/create', data=delivery_itens_data)
        delivery_itens_created = db.session.query(DeliveryItem).all()

        with delivery_itens.session_transaction() as session:
            print(session.get('_flashes'))

        assert response.status_code == 302
        assert len(delivery_itens_created) == 1


def test_delivery_itens_delete_route(delivery_itens):
    with delivery_itens.application.app_context():
        client = Client(
            name = 'client_test1',
            CPF_CNPJ = '123456789',
            email = 'test1@gmail.com',
            phone = '789456123',
        )

        db.session.add(client)
        db.session.flush()

        order_service = OrderService(
            client_id=client.id,
            weight_total=100,
            cubage_total=100,
            origin='SP',
            destination='RJ',
            distance=500,
            price=1000,
            status=OrderStatus.PENDING,
        )

        db.session.add(order_service)
        db.session.flush()

        order_item = OrderItem(
            order_service_id=order_service.id,
            quantity = 10,
            weight = 10.0,
            cubage = 10.0,
            price_item = 100,
        )

        driver = Driver(
            name='driver_test1',
            cnh='123456789',
            phone='987654321',
            admission_date=datetime.datetime.now(),
            licence_category=DrivingLicenceCategory.E,
            license_expiration_date=datetime.datetime.now(),
            status=DriverStatus.AVAILABLE
        )

        vehicle = Vehicle(
            cargo_capacity_kg=1000,
            cargo_capacity_m3=1000,
            license_plate='TXQ-8451',
            model='MERCEDES',
            status=VehicleStatus.AVAILABLE,
            axle_count=6,
            odometer=20000,
            fuel_type=FuelType.DIESEL,
        )

        db.session.add_all([
            order_item,
            driver,
            vehicle
        ])

        db.session.flush()

        delivery = Delivery(
            order_service_id = order_service.id,
            driver_id = driver.id,
            vehicle_id =  vehicle.id,
        )

        db.session.add(delivery)
        db.session.flush()

        delivery_itens_data = {
            'order_item_id': order_item.id,
            'delivery_id': delivery.id,
            'weight': 10.0,
            'cubage': 10.0,
            'quantity': 10,
        }

        delivery_itens.post('/delivery_itens/create', data=delivery_itens_data)
        response = delivery_itens.post('/delivery_itens/1/delete')

        delivery_itens_created = db.session.query(DeliveryItem).all()

        with delivery_itens.session_transaction() as session:
            print(session.get('_flashes'))

        assert response.status_code == 302
        assert len(delivery_itens_created) == 0