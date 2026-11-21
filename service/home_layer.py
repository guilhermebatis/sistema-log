from app.models.delivery import Delivery, StatusDelivery
from app.models.order_service import OrderService
from app.models.client import Client
from app.models.vehicle import Vehicle
from app import db


def count_pending_deliveries():

    query = db.func.count(Delivery.id)

    deliveries_cont = (db.select(query)
                        .where(Delivery.status == StatusDelivery.PENDING))

    data = db.session.scalar(deliveries_cont)

    return data


def count_in_progress_deliveries():

    query = db.func.count(Delivery.id)

    deliveries_cont = (db.select(query)
                       .where(Delivery.status == StatusDelivery.IN_PROGRESS))

    data = db.session.scalar(deliveries_cont)

    return data


def count_completed_deliveries():
    query = db.func.count(Delivery.id)

    deliveries_cont = (db.select(query)
                       .where(Delivery.status == StatusDelivery.COMPLETED))

    data = db.session.scalar(deliveries_cont)

    return data


def count_orders():
    query = db.func.count(OrderService.id)

    data = db.session.scalar(db.select(query))

    return data


def count_clients():
    query = db.func.count(Client.id)

    data = db.session.scalar(db.select(query))

    return data


def count_vehicles():
    query = db.func.count(Vehicle.id)

    data = db.session.scalar(db.select(query))
    return data


def get_dashboard_data():

    pending_deliveries = count_pending_deliveries()
    in_progress_deliveries = count_in_progress_deliveries()
    completed_deliveries = count_completed_deliveries()
    orders = count_orders()
    clients = count_clients()
    vehicles = count_vehicles()

    return {'pending_deliveries': pending_deliveries,
            'in_progress_deliveries': in_progress_deliveries,
            'completed_deliveries': completed_deliveries,
            'orders': orders,
            'clients': clients,
            'vehicles': vehicles,}