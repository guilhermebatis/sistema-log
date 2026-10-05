from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.delivery import Delivery, StatusDelivery
from app.models.driver import Driver
from app.models.vehicle import Vehicle
from app.models.order_service import OrderService, OrderItem


delivery_bp = Blueprint('delivery', __name__, url_prefix='/delivery')

@delivery_bp.route('/')
def index():
    delivery_data = db.session.query(Delivery).all()


    return render_template('delivery/index.html',
                           deliveries=delivery_data)

@delivery_bp.route('/<int:id>/info', methods=['GET'])
def info(id):
    delivery_data = db.session.get(Delivery, id)
    driver_data = delivery_data.driver_id
    vehicle_data = delivery_data.vehicle_id

    return render_template('delivery/info.html',
                           deliveries=delivery_data,
                           drivers=driver_data,
                           vehicles=vehicle_data)


@delivery_bp.route('/create', methods=['GET', 'POST'])
def create_delivery():

    if request.method == 'GET':
        order_services_data = db.session.query(OrderService).all()
        driver_data = db.session.query(Driver).all()
        vehicle_data = db.session.query(Vehicle).all()

        return render_template('delivery/create.html',
                               order_services=order_services_data,
                               drivers=driver_data,
                               vehicles=vehicle_data)

    if request.method == 'POST':

        delivery_order_service_id = request.form.get('order_service_id', '').strip()
        delivery_status = request.form.get('status', '').strip()
        delivery_driver_id = request.form.get('driver_id', '').strip()
        delivery_vehicle_id = request.form.get('vehicle_id', '').strip()

        if not delivery_order_service_id:
            flash('Não foi possivel criar a entrega, falta o campo de ordem de serviço', 'danger')
            return redirect(url_for('delivery.create_delivery'))
        if not delivery_status:
            flash('Não foi possivel criar a entrega, falta o campo de status', 'danger')
            return redirect(url_for('delivery.create_delivery'))

        try:
            delivery_order_service_id = int(delivery_order_service_id)
            delivery_status = StatusDelivery(delivery_status)

            if not delivery_driver_id:
                delivery_driver_id = None
            else:
                delivery_driver_id = int(delivery_driver_id)

            if not delivery_vehicle_id:
                delivery_vehicle_id = None
            else:
                delivery_vehicle_id = int(delivery_vehicle_id)

        except ValueError:
            flash('Não foi possivel criar a entrega', 'danger')
            return redirect(url_for('delivery.create_delivery'))

        new_delivery = Delivery(
            order_service_id = delivery_order_service_id,
            status = delivery_status,
            driver_id = delivery_driver_id,
            vehicle_id = delivery_vehicle_id,
        )

        try:
            db.session.add(new_delivery)
            db.session.commit()
            flash('Entrega criado com sucesso', 'success')
            return redirect(url_for('delivery.index'))

        except IntegrityError:
            db.session.rollback()
            flash('Não foi possivel criar a entrega', 'danger')
            return redirect(url_for('delivery.create_delivery'))


@delivery_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_delivery(id):

    if request.method == 'GET':
        delivery_data = db.session.get(Delivery, id)

        if not delivery_data:
            flash('Não foi possivel localizar a entrega', 'danger')
            return redirect(url_for('delivery.index'))

        order_services_data = db.session.query(OrderService).all()
        driver_data = db.session.query(Driver).all()
        vehicle_data = db.session.query(Vehicle).all()

        return render_template('delivery/update.html',
                               id=id,
                               deliveries=delivery_data,
                               order_services=order_services_data,
                               drivers=driver_data,
                               vehicles=vehicle_data)

    if request.method == 'POST':

        data = db.session.get(Delivery, id)

        if not data:
            flash('Não foi possivel localizar a entrega', 'danger')
            return redirect(url_for('delivery.index'))

        delivery_order_service_id = request.form.get('order_service_id', '').strip()
        delivery_status = request.form.get('status', '').strip()
        delivery_driver_id = request.form.get('driver_id', '').strip()
        delivery_vehicle_id = request.form.get('vehicle_id', '').strip()

        if not delivery_order_service_id:
            flash('Não foi possivel criar a entrega, falta o campo de ordem de serviço', 'danger')
            return redirect(url_for('delivery.update_delivery', id=id))
        if not delivery_status:
            flash('Não foi possivel criar a entrega, falta o campo de status', 'danger')
            return redirect(url_for('delivery.update_delivery', id=id))

        try:
            delivery_order_service_id = int(delivery_order_service_id)
            delivery_status = StatusDelivery(delivery_status)

            if not delivery_driver_id:
                delivery_driver_id = None
            else:
                delivery_driver_id = int(delivery_driver_id)

            if not delivery_vehicle_id:
                delivery_vehicle_id = None
            else:
                delivery_vehicle_id = int(delivery_vehicle_id)
        except ValueError:
            flash('Não foi possivel criar a entrega', 'danger')
            return redirect(url_for('delivery.update_delivery', id=id))

        data.order_service_id = delivery_order_service_id
        data.status = delivery_status
        data.driver_id = delivery_driver_id
        data.vehicle_id = delivery_vehicle_id

        try:
            db.session.commit()
            flash('Entrega atualizada com sucesso', 'success')
            return redirect(url_for('delivery.index'))

        except IntegrityError:
            db.session.rollback()
            flash('Não foi possível atualizar a entrega', 'danger')
            return redirect(url_for('delivery.update_delivery', id=id))


@delivery_bp.route('/<int:id>/delete', methods=['POST'])
def delete_delivery(id):

    data = db.session.get(Delivery, id)

    if not data:
        flash('Não foi possivel localizar a entrega', 'danger')
        return redirect(url_for('delivery.index'))

    try:
        db.session.delete(data)
        db.session.commit()
        flash('Entrega deletado com sucesso', 'success')
        return redirect(url_for('delivery.index'))
    except IntegrityError:
        flash('Não foi possivel deletar a entrega', 'danger')
        return redirect(url_for('delivery.index'))
