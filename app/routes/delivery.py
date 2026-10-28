from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.extensions import db
from app.models.delivery import Delivery, DeliveryItem, StatusDelivery
from app.models.order_service import OrderItem
from service.delivery_layer import create_delivery, update_delivery, delete_delivery


delivery_bp = Blueprint('delivery', __name__, url_prefix='/delivery')


@delivery_bp.route('/')
def index():
    delivery_itens_data = db.session.query(DeliveryItem).all()
    delivery_data = db.session.query(Delivery).all()

    return render_template('delivery/index.html',
                           deliveries=delivery_data,
                           delivery_itens=delivery_itens_data)


@delivery_bp.route('<int:id>/info', methods=['GET'])
def info(id):
    delivery_itens_data = db.session.get(DeliveryItem, id)

    if not delivery_itens_data:
        flash('Não foi possivel localizar o item da entrega')
        return redirect(url_for('delivery.index'))

    delivery_data = delivery_itens_data.delivery

    return render_template('delivery/info.html',
                           delivery=delivery_data,
                           delivery_itens=delivery_itens_data)


@delivery_bp.route('/create', methods=['GET', 'POST'])
def create_delivery():
    if request.method == 'GET':
        deliveries_data  = db.session.query(Delivery).all()
        order_items_data  = db.session.query(OrderItem).all()

        return render_template('delivery/create.html',
                               deliveries=deliveries_data,
                               order_items=order_items_data,)

    if request.method == 'POST':

        delivery_order_service_id = request.form.get('order_service_id', '').strip()
        delivery_status = request.form.get('status', '').strip()
        delivery_driver_id = request.form.get('driver_id', '').strip()
        delivery_vehicle_id = request.form.get('vehicle_id', '').strip()

        try:
            delivery_order_service_id = int(delivery_order_service_id)
            delivery_status = StatusDelivery(delivery_status)
            delivery_driver_id = int(delivery_driver_id)
            delivery_vehicle_id = int(delivery_vehicle_id)
        except ValueError:
            flash('Não foi possivel criar o item da entrega, somente numeros nos campos numericos', 'danger')
            return redirect(url_for('delivery.create_delivery'))

        new_delivery = Delivery(
            order_service_id = delivery_order_service_id,
            status = delivery_status,
            driver_id = delivery_driver_id,
            vehicle_id = delivery_vehicle_id,
        )

        if create_delivery(new_delivery):
            return redirect(url_for('delivery.index'))
        else:
            return redirect(url_for('delivery.create_delivery'))


@delivery_bp.route('<int:id>/update', methods=['GET', 'POST'])
def update_delivery(id):
    if request.method == 'GET':
        delivery_itens_data = db.session.get(DeliveryItem, id)
        if not delivery_itens_data:
            flash('Não foi possivel localizar o item', 'danger')
            return redirect(url_for('delivery.index'))
        order_items_data = db.session.query(OrderItem).all()
        deliveries_data = db.session.query(Delivery).all()

        return render_template(
            'delivery/update.html',
            delivery_item=delivery_itens_data,
            order_items=order_items_data,
            deliveries=deliveries_data,
        )

    if request.method == 'POST':

        delivery_order_service_id = request.form.get('order_service_id', '').strip()
        delivery_status = request.form.get('status', '').strip()
        delivery_driver_id = request.form.get('driver_id', '').strip()
        delivery_vehicle_id = request.form.get('vehicle_id', '').strip()

        try:
            delivery_order_service_id = int(delivery_order_service_id)
            delivery_status = StatusDelivery(delivery_status)
            delivery_driver_id = int(delivery_driver_id)
            delivery_vehicle_id = int(delivery_vehicle_id)
        except ValueError:
            flash('Não foi possivel criar o item da entrega, somente numeros nos campos numericos', 'danger')
            return redirect(url_for('delivery_itens.update_delivery', id=id))

        var_update_delivery = Delivery(
            id = id,
            order_service_id = delivery_order_service_id,
            status = delivery_status,
            driver_id = delivery_driver_id,
            vehicle_id = delivery_vehicle_id,
        )

        if update_delivery(var_update_delivery):
            return redirect(url_for('delivery.index'))
        else:
            return redirect(url_for('delivery.create_delivery'))


@delivery_bp.route('/<int:id>/delete', methods=['POST'])
def delete_delivery(id):
    data = db.session.get(Delivery, id)
    if delete_delivery(data):
        return redirect(url_for('delivery.index'))
    else:
        return redirect(url_for('delivery.index'))