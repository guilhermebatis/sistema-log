from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.extensions import db
from app.models.delivery import Delivery, DeliveryItem
from app.models.order_service import OrderItem
from service.delivery_layer import create_delivery_item, update_delivery_item, delete_delivery_item


delivery_itens_bp = Blueprint('delivery_itens', __name__, url_prefix='/delivery_itens')


@delivery_itens_bp.route('/')
def index():
    delivery_itens_data = db.session.query(DeliveryItem).all()
    delivery_data = db.session.query(Delivery).all()

    return render_template('delivery_itens/index.html',
                           deliveries=delivery_data,
                           delivery_itens=delivery_itens_data)


@delivery_itens_bp.route('<int:id>/info', methods=['GET'])
def info(id):
    delivery_itens_data = db.session.get(DeliveryItem, id)

    if not delivery_itens_data:
        flash('Não foi possivel localizar o item da entrega')
        return redirect(url_for('delivery_itens.index'))

    delivery_data = delivery_itens_data.delivery

    return render_template('delivery_itens/info.html',
                           delivery=delivery_data,
                           delivery_itens=delivery_itens_data)


@delivery_itens_bp.route('/create', methods=['GET', 'POST'])
def create_delivery_itens():
    if request.method == 'GET':
        deliveries_data  = db.session.query(Delivery).all()
        order_items_data  = db.session.query(OrderItem).all()

        return render_template('delivery_itens/create.html',
                               deliveries=deliveries_data,
                               order_items=order_items_data,)

    if request.method == 'POST':
        delivery_itens_order_item_id = request.form.get('order_item_id', '').strip()
        delivery_itens_delivery_id = request.form.get('delivery_id', '').strip()
        delivery_itens_weight = request.form.get('weight', '').strip()
        delivery_itens_cubage = request.form.get('cubage', '').strip()
        delivery_itens_quantity = request.form.get('quantity', '').strip()

        try:
            delivery_itens_order_item_id = int(delivery_itens_order_item_id)
            delivery_itens_delivery_id = int(delivery_itens_delivery_id)
            delivery_itens_weight = float(delivery_itens_weight)
            delivery_itens_cubage = float(delivery_itens_cubage)
            delivery_itens_quantity = int(delivery_itens_quantity)
        except ValueError:
            flash('Não foi possivel criar o item da entrega, somente numeros nos campos numericos', 'danger')
            return redirect(url_for('delivery_itens.create_delivery_itens'))

        new_delivery_itens = DeliveryItem(
            order_item_id = delivery_itens_order_item_id,
            delivery_id = delivery_itens_delivery_id,
            weight = delivery_itens_weight,
            cubage = delivery_itens_cubage,
            quantity = delivery_itens_quantity,
        )

        if create_delivery_item(new_delivery_itens):
            return redirect(url_for('delivery_itens.index'))

        return redirect(url_for('delivery_itens.create_delivery_itens'))


@delivery_itens_bp.route('<int:id>/update', methods=['GET', 'POST'])
def update_delivery_itens(id):
    if request.method == 'GET':

        delivery_itens_data = db.session.get(DeliveryItem, id)

        if not delivery_itens_data:
            flash('Não foi possivel localizar o item', 'danger')
            return redirect(url_for('delivery_itens.index'))
        order_items_data = db.session.query(OrderItem).all()
        deliveries_data = db.session.query(Delivery).all()

        return render_template(
            'delivery_itens/update.html',
            delivery_item=delivery_itens_data,
            order_items=order_items_data,
            deliveries=deliveries_data,
        )

    if request.method == 'POST':


        delivery_itens_order_item_id = request.form.get('order_item_id', '').strip()
        delivery_itens_delivery_id = request.form.get('delivery_id', '').strip()
        delivery_itens_weight = request.form.get('weight', '').strip()
        delivery_itens_cubage = request.form.get('cubage', '').strip()
        delivery_itens_quantity = request.form.get('quantity', '').strip()

        try:
            delivery_itens_order_item_id = int(delivery_itens_order_item_id)
            delivery_itens_delivery_id = int(delivery_itens_delivery_id)
            delivery_itens_weight = float(delivery_itens_weight)
            delivery_itens_cubage = float(delivery_itens_cubage)
            delivery_itens_quantity = int(delivery_itens_quantity)

        except ValueError:
            flash('Não foi possivel criar o item da entrega, somente numeros nos campos numericos', 'danger')
            return redirect(url_for('delivery_itens.update_delivery_itens', id=id))

        delivery_item = DeliveryItem(
            id = id,
            order_item_id = delivery_itens_order_item_id,
            delivery_id = delivery_itens_delivery_id,
            weight = delivery_itens_weight,
            quantity = delivery_itens_quantity,
            cubage = delivery_itens_cubage,
        )

        if update_delivery_item(delivery_item):
            return redirect(url_for('delivery_itens.index'))
        else:
            return redirect(url_for('delivery_itens.update_delivery_itens', id=id))


@delivery_itens_bp.route('/<int:id>/delete', methods=['POST'])
def delete_delivery_itens(id):
    delivery_item = db.session.get(DeliveryItem, id)
    if delete_delivery_item(delivery_item):
        return redirect(url_for('delivery_itens.index'))
    else:
        return redirect(url_for('delivery_itens.index', id=id))