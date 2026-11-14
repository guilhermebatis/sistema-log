from flask import Blueprint, render_template, request, redirect, url_for, flash

from app import db
from app.models import Delivery
from app.models.order_service import OrderService, OrderStatus, OrderItem
from app.models.client import Client
from service.order_layer import create_order_service, update_order_service, delete_order_service
from decimal import Decimal


orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route('/')
def index():
    data = db.session.query(OrderService).all()
    return render_template('orders/index.html', data=data)


@orders_bp.route('/<int:order_id>/info', methods=['GET'])
def order_info(order_id):

    order_data = db.session.get(OrderService, order_id)
    if not order_data:
        flash('Não foi possivel localizar a ordem', 'danger')
        return redirect(url_for('orders.index'))

    delivery_data = order_data.deliveries
    order_items_data = order_data.order_items

    return render_template('orders/info.html',
                           order_data=order_data,
                           delivery_data=delivery_data,
                           order_items_data=order_items_data,)


@orders_bp.route('/create', methods=['GET', 'POST'])
def create_order():
    if request.method == 'GET':
        clients = db.session.query(Client).all()
        return render_template('orders/create.html',  clients=clients)


    if request.method == 'POST':

        order_client_id = request.form.get('client_id', '')
        order_origin = request.form.get('origin', '')
        order_destination = request.form.get('destination', '')
        order_distance = request.form.get('distance', '')
        order_status = request.form.get('status', '')

        try:
            order_client_id = int(order_client_id)
            order_distance = Decimal(order_distance)
            order_status = OrderStatus(order_status)
        except ValueError:
            flash('Error ao criar a ordem de serviço', 'danger')
            return redirect(url_for('orders.create_order'))

        order_service = OrderService(
        client_id = order_client_id,
        origin = order_origin,
        destination = order_destination,
        distance = order_distance,
        status = order_status,
       )

        if create_order_service(order_service):
            return redirect(url_for('orders.index'))
        else:
            return redirect(url_for('orders.create_order'))


@orders_bp.route('/<int:order_id>/update', methods=['GET', 'POST'])
def update_order(order_id):

    if request.method == 'GET':

        data = db.session.get(OrderService, order_id)

        if not data:
            flash('Não foi possivel localizar a ordem', 'danger')
            return redirect(url_for('orders.index'))

        clients = db.session.query(Client).all()

        return render_template('orders/update.html', order=data, clients=clients)

    if request.method == 'POST':

        data = db.session.get(OrderService, order_id)

        if not data:
            flash('Ordem não localizado', 'danger')
            return redirect(url_for('orders.index'))

        order_client_id = request.form.get('client_id', '')
        order_origin = request.form.get('origin', '')
        order_destination = request.form.get('destination', '')
        order_distance = request.form.get('distance', '')
        order_status = request.form.get('status', '')

        try:
            order_client_id = int(order_client_id)
            order_distance = float(order_distance)
            order_status = OrderStatus(order_status)
        except ValueError:
            flash('Error ao criar a ordem de serviço', 'danger')
            return redirect(url_for('orders.update_order', order_id=order_id))

        data.client_id = order_client_id
        data.origin = order_origin
        data.destination = order_destination
        data.distance = order_distance
        data.status = order_status

        if update_order_service(data):
            return redirect(url_for('orders.index'))
        else:
            return redirect(url_for('orders.update_order', order_id=order_id))


@orders_bp.route('/<int:order_id>/delete', methods=['POST'])
def delete_order(order_id):

    data = db.session.get(OrderService, order_id)

    if delete_order_service(data):
        return redirect(url_for('orders.index'))
    else:
        return redirect(url_for('orders.index'))