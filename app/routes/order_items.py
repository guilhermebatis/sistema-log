from flask import Blueprint, render_template, request, redirect, url_for, flash

from app import db
from app.models.order_service import OrderService, OrderItem
from service.order_layer import create_order_item_service, update_order_item_service, delete_order_item_service
from decimal import Decimal


order_items_bp  = Blueprint('order_items', __name__, url_prefix='/order_items')


@order_items_bp.route("/")
def index():
    data = db.session.query(OrderItem).all()
    return render_template('order_item/index.html', data=data)


@order_items_bp.route("/create", methods=['GET', 'POST'])
def create_order_item():
    if request.method == 'GET':
        order_services = db.session.query(OrderService).all()
        return render_template('order_item/create.html', order_services=order_services)

    if request.method == 'POST':

        order_item_order_service_id = request.form.get('order_service_id', '').strip()
        order_item_quantity = request.form.get('quantity', '').strip()
        order_item_description = request.form.get('description', '').strip()
        order_item_weight = request.form.get('weight', '').strip()
        order_item_cubage = request.form.get('cubage', '').strip()
        order_item_price_item = request.form.get('price_item', '').strip()

        try:
            order_item_order_service_id = int(order_item_order_service_id)
            order_item_quantity = int(order_item_quantity)
            order_item_weight = Decimal(order_item_weight)
            order_item_cubage = Decimal(order_item_cubage)
            order_item_price_item = Decimal(order_item_price_item)
        except ValueError:
            flash('')
            return redirect(url_for('order_items.create_order_item'))

        order_item = OrderItem(
            order_service_id = order_item_order_service_id,
            quantity = order_item_quantity,
            description = order_item_description,
            weight = order_item_weight,
            cubage = order_item_cubage,
            price_item = order_item_price_item,
        )

        if create_order_item_service(order_item):
            return redirect(url_for('order_items.index'))
        else:
            return redirect(url_for('order_items.create_order_item'))


@order_items_bp.route("/<int:order_item_id>/update", methods=['GET', 'POST'])
def update_order_item(order_item_id):
    if request.method == 'GET':
        order_item_data = db.session.get(OrderItem, order_item_id)

        if not order_item_data:
            flash('Não foi possível localizar o item da ordem', 'danger')
            return redirect(url_for('order_items.index'))

        order_service_id = order_item_data.order_service_id
        order_service_data = db.session.get(OrderService, order_service_id)

        if not order_service_data:
            flash('Não foi possível localizar a order de serviço', 'danger')
            return redirect(url_for('order_items.index'))

        order_services = db.session.query(OrderService).all()

        return render_template('order_item/update.html',
                               data=order_item_data,
                               data_order = order_service_data,
                               order_services=order_services)

    if request.method == 'POST':

        data = db.session.get(OrderItem, order_item_id)

        if not data:
            flash('Não foi possivel achar o item da order', 'danger')
            return redirect(url_for('order_items.index'))

        order_item_order_service_id = request.form.get('order_service_id', '').strip()
        order_item_quantity = request.form.get('quantity', '').strip()
        order_item_description = request.form.get('description', '').strip()
        order_item_weight = request.form.get('weight', '').strip()
        order_item_cubage = request.form.get('cubage', '').strip()
        order_item_price_item = request.form.get('price_item', '').strip()

        try:
            order_item_order_service_id = int(order_item_order_service_id)
            order_item_quantity = int(order_item_quantity)
            order_item_weight = Decimal(order_item_weight)
            order_item_cubage = Decimal(order_item_cubage)
            order_item_price_item = Decimal(order_item_price_item)
        except ValueError:
            flash('Não foi possivel atualizar o item da ordem', 'danger')
            return redirect(url_for('order_items.update_order_item', order_item_id=order_item_id))

        data.order_service_id = order_item_order_service_id
        data.quantity = order_item_quantity
        data.description = order_item_description
        data.weight = order_item_weight
        data.cubage = order_item_cubage
        data.price_item = order_item_price_item

        if update_order_item_service(data):
            return redirect(url_for('order_items.index'))
        else:
            return redirect(url_for('order_items.update_order_item', order_item_id=order_item_id))


@order_items_bp.route("/<int:order_item_id>/delete", methods=['POST'])
def delete_order_item(order_item_id):
    data = db.session.get(OrderItem, order_item_id)

    if delete_order_item_service(data):
        return redirect(url_for('order_items.index'))
    else:
        return redirect(url_for('order_items.index'))
