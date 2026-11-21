from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.extensions import db
from app.models import OrderService, Driver, Vehicle
from app.models.delivery import Delivery, DeliveryItem, StatusDelivery
from app.models.order_service import OrderItem
from service.delivery_layer import create_delivery_service, update_delivery_service, delete_delivery_service
from flask_login import login_required


delivery_bp = Blueprint('delivery', __name__, url_prefix='/delivery')


@delivery_bp.route('/')
@login_required
def index():
    delivery_itens_data = db.session.query(DeliveryItem).all()
    delivery_data = db.session.query(Delivery).all()

    return render_template('delivery/index.html',
                           deliveries=delivery_data,
                           delivery_itens=delivery_itens_data)


@delivery_bp.route('<int:id>/info', methods=['GET'])
@login_required
def info(id):
    delivery_data = db.session.get(Delivery, id)

    if not delivery_data:
        flash('Não foi possivel localizar a entrega')
        return redirect(url_for('delivery.index'))


    return render_template('delivery/info.html',
                           deliveries=delivery_data,
                           )


@delivery_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_delivery():
    if request.method == 'GET':
        order_service_data  = db.session.query(OrderService).all()
        order_items_data  = db.session.query(OrderItem).all()
        drivers_data = db.session.query(Driver).all()
        vehicle_data = db.session.query(Vehicle).all()

        return render_template('delivery/create.html',
                               order_services=order_service_data,
                               order_items=order_items_data,
                               drivers=drivers_data,
                               vehicles=vehicle_data)

    if request.method == 'POST':

        delivery_order_service_id = request.form.get('order_service_id', '').strip()
        delivery_status = request.form.get('status', StatusDelivery.PENDING)
        delivery_driver_id = request.form.get('driver_id', '').strip()
        delivery_vehicle_id = request.form.get('vehicle_id', '').strip()

        new_delivery = Delivery(
            order_service_id = delivery_order_service_id,
            status = delivery_status,
            driver_id = delivery_driver_id,
            vehicle_id = delivery_vehicle_id,
        )

        if create_delivery_service(new_delivery):
            return redirect(url_for('delivery.index'))
        else:
            return redirect(url_for('delivery.create_delivery'))


@delivery_bp.route('<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_delivery(id):
    if request.method == 'GET':
        delivery_data = db.session.get(Delivery, id)
        if not delivery_data:
            flash('Não foi possivel localizar a entrega', 'danger')
            return redirect(url_for('delivery.index'))

        order_service_data  = db.session.query(OrderService).all()
        drivers_data = db.session.query(Driver).all()
        vehicle_data = db.session.query(Vehicle).all()

        return render_template(
            'delivery/update.html',
            order_services=order_service_data,
            drivers=drivers_data,
            vehicles=vehicle_data,
            deliveries=delivery_data,
        )

    if request.method == 'POST':

        delivery_order_service_id = request.form.get('order_service_id', '').strip()
        delivery_status = request.form.get('status', '').strip()
        delivery_driver_id = request.form.get('driver_id', '').strip()
        delivery_vehicle_id = request.form.get('vehicle_id', '').strip()

        var_update_delivery = Delivery(
            id = id,
            order_service_id = delivery_order_service_id,
            status = delivery_status,
            driver_id = delivery_driver_id,
            vehicle_id = delivery_vehicle_id,
        )

        if update_delivery_service(var_update_delivery):
            return redirect(url_for('delivery.index'))
        else:
            return redirect(url_for('delivery.create_delivery'))


@delivery_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_delivery(id):
    data = db.session.get(Delivery, id)
    if delete_delivery_service(data):
        return redirect(url_for('delivery.index'))
    else:
        return redirect(url_for('delivery.index'))