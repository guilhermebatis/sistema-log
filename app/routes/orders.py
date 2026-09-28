from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.order_service import OrderService, OrderStatus
from app.models.client import Client


orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/')
def index():
    data = db.session.query(OrderService).all()
    return render_template('orders/index.html', data=data)


@orders_bp.route('/create', methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':

        order_client_id = request.form.get('client_id', '')
        order_weight_total = request.form.get('weight_total', '')
        order_cubage_total = request.form.get('cubage_total', '')
        order_origin = request.form.get('origin', '')
        order_destination = request.form.get('destination', '')
        order_distance = request.form.get('distance', '')
        order_price = request.form.get('price', '')
        order_status = request.form.get('status', '')

        if not order_origin:
            flash('Não foi possivel criar a ordem de serviço, falta o campo origem', 'danger')
            return redirect(url_for('orders.create_order'))
        if not order_destination:
            flash('Não foi possivel criar a ordem de serviço, falta o campo destino', 'danger')
            return redirect(url_for('orders.create_order'))
        if not order_distance:
            flash('Não foi possivel criar a ordem de serviço, falta o campo distancia', 'danger')
            return redirect(url_for('orders.create_order'))
        if not order_status:
            flash('Não foi possivel criar a ordem de serviço, falta o campo status', 'danger')
            return redirect(url_for('orders.create_order'))

        try:
            if order_client_id:
                order_client_id = int(order_client_id)
            else:
                order_client_id = None

            if order_weight_total:
                order_weight_total = float(order_weight_total)
                if order_weight_total < 0:
                    flash('Não foi possivel criar a ordem, o campo peso tem que ser positivo')
                    return redirect(url_for('orders.create_order'))
            else:
                order_weight_total = None

            if order_cubage_total:
                order_cubage_total = float(order_cubage_total)
                if order_cubage_total < 0:
                    flash('Não foi possivel criar a ordem, o campo cubagem tem que ser positivo')
                    return redirect(url_for('orders.create_order'))
            else:
                order_cubage_total = None

            if order_price:
                order_price = float(order_price)
                if order_price < 0:
                    flash('Não foi possivel criar a ordem, o campo preço tem que ser positivo')
                    return redirect(url_for('orders.create_order'))
            else:
                order_price = None

            if order_distance:
                order_distance = float(order_distance)
                if order_distance < 0:
                    flash('Não foi possivel criar a ordem, o campo distancia tem que ser positivo')
                    return redirect(url_for('orders.create_order'))


            order_status = OrderStatus(order_status)

        except ValueError:
            flash('Error ao criar a ordem de serviço', 'danger')
            return redirect(url_for('orders.create_order'))

        try:
            new_order = OrderService(
            client_id = order_client_id,
            weight_total = order_weight_total,
            cubage_total = order_cubage_total,
            origin = order_origin,
            destination = order_destination,
            distance = order_distance,
            price = order_price,
            status = order_status,
            )

            db.session.add(new_order)
            db.session.commit()
            flash('Ordem criado com sucesso', 'success')
            return redirect(url_for('orders.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Error a criar a ordem', 'danger')
            return redirect(url_for('orders.create_order'))

    clients = db.session.query(Client).all()
    return render_template('orders/create.html',  clients=clients)


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
        order_weight_total = request.form.get('weight_total', '')
        order_cubage_total = request.form.get('cubage_total', '')
        order_origin = request.form.get('origin', '')
        order_destination = request.form.get('destination', '')
        order_distance = request.form.get('distance', '')
        order_price = request.form.get('price', '')
        order_status = request.form.get('status', '')

        if not order_origin:
            flash('Não foi possivel atualizar a ordem de serviço, falta o campo origem', 'danger')
            return redirect(url_for('orders.update_order', order_id=order_id))
        if not order_destination:
            flash('Não foi possivel atualizar a ordem de serviço, falta o campo destino', 'danger')
            return redirect(url_for('orders.update_order', order_id=order_id))
        if not order_distance:
            flash('Não foi possivel atualizar a ordem de serviço, falta o campo distancia', 'danger')
            return redirect(url_for('orders.update_order', order_id=order_id))
        if not order_status:
            flash('Não foi possivel atualizar a ordem de serviço, falta o campo status', 'danger')
            return redirect(url_for('orders.update_order', order_id=order_id))

        try:
            if order_client_id:
                order_client_id = int(order_client_id)
            else:
                order_client_id = None

            if order_weight_total:
                order_weight_total = float(order_weight_total)
                if order_weight_total < 0:
                    flash('Não foi possivel atualizar a ordem, o campo peso tem que ser positivo', 'danger')
                    return redirect(url_for('orders.update_order', order_id=order_id))
            else:
                order_weight_total = None

            if order_cubage_total:
                order_cubage_total = float(order_cubage_total)
                if order_cubage_total < 0:
                    flash('Não foi possivel atualizar a ordem, o campo cubagem tem que ser positivo', 'danger')
                    return redirect(url_for('orders.update_order', order_id=order_id))
            else:
                order_cubage_total = None

            if order_price:
                order_price = float(order_price)
                if order_price < 0:
                    flash('Não foi possivel atualizar a ordem, o campo preço tem que ser positivo', 'danger')
                    return redirect(url_for('orders.update_order', order_id=order_id))
            else:
                order_price = None

            if order_distance:
                order_distance = float(order_distance)
                if order_distance < 0:
                    flash('Não foi possivel atualizar a ordem, o campo distancia tem que ser positivo', 'danger')
                    return redirect(url_for('orders.update_order', order_id=order_id))

            order_status = OrderStatus(order_status)

        except ValueError:
            flash('Error ao atualizar a ordem de serviço', 'danger')
            return redirect(url_for('orders.update_order', order_id=order_id))

        data.client_id = order_client_id
        data.weight_total = order_weight_total
        data.cubage_total = order_cubage_total
        data.origin = order_origin
        data.destination = order_destination
        data.distance = order_distance
        data.price = order_price
        data.status = order_status
        try:
            db.session.commit()
            flash('Ordem de serviço atualizado com sucesso!', 'success')
            return redirect(url_for('orders.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Error ao atualizar a ordem', 'danger')
            return redirect(url_for('orders.update_order', order_id=order_id))


@orders_bp.route('/<int:order_id>/delete', methods=['POST'])
def delete_order(order_id):

    data = db.session.get(OrderService, order_id)

    if not data:
        flash('Não foi possivel localizar a ordem', 'danger')
        return redirect(url_for('orders.index'))

    try:
        db.session.delete(data)
        db.session.commit()
        flash('Ordem deletado com sucesso!', 'success')
        return redirect(url_for('orders.index'))
    except IntegrityError:
        db.session.rollback()
        flash('Error ao deletar a ordem', 'danger')
        return redirect(url_for('orders.index'))
