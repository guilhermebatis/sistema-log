from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.delivery import Delivery, DeliveryItem
from app.models.order_service import OrderItem

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

        if not delivery_itens_order_item_id:
            flash('Não foi possivel criar o item da entrega, falta o campo item da ordem', 'danger')
            return redirect(url_for('delivery_itens.create_delivery_itens'))
        if not delivery_itens_delivery_id:
            flash('Não foi possivel criar o item da entrega, falta o campo entrega', 'danger')
            return redirect(url_for('delivery_itens.create_delivery_itens'))


        try:
            delivery_itens_order_item_id = int(delivery_itens_order_item_id)
            delivery_itens_delivery_id = int(delivery_itens_delivery_id)
            if not delivery_itens_weight:
                delivery_itens_weight = None
            else:
                delivery_itens_weight = float(delivery_itens_weight)

            if not delivery_itens_cubage:
                delivery_itens_cubage = None
            else:
                delivery_itens_cubage = float(delivery_itens_cubage)

        except ValueError:
            flash('Não foi possivel criar o item da entrega, somente numeros nos campos numericos', 'danger')
            return redirect(url_for('delivery_itens.create_delivery_itens'))

        new_delivery_itens = DeliveryItem(
            order_item_id = delivery_itens_order_item_id,
            delivery_id = delivery_itens_delivery_id,
            weight = delivery_itens_weight,
            cubage = delivery_itens_cubage,
        )

        try:
            db.session.add(new_delivery_itens)
            db.session.commit()
            flash('Item criado com sucesso', 'success')
            return redirect(url_for('delivery_itens.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Não foi possivel criar o item da entrega, error ao criar', 'danger')
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
        data = db.session.get(DeliveryItem, id)
        if not data:
            flash('Não foi possivel localizar o item', 'danger')
            return redirect(url_for('delivery_itens.index'))

        delivery_itens_order_item_id = request.form.get('order_item_id', '').strip()
        delivery_itens_delivery_id = request.form.get('delivery_id', '').strip()
        delivery_itens_weight = request.form.get('weight', '').strip()
        delivery_itens_cubage = request.form.get('cubage', '').strip()

        if not delivery_itens_order_item_id:
            flash('Não foi possivel criar o item da entrega, falta o campo item da ordem', 'danger')
            return redirect(url_for('delivery_itens.update_delivery_itens', id=id))
        if not delivery_itens_delivery_id:
            flash('Não foi possivel criar o item da entrega, falta o campo entrega', 'danger')
            return redirect(url_for('delivery_itens.update_delivery_itens', id=id))

        try:
            delivery_itens_order_item_id = int(delivery_itens_order_item_id)
            delivery_itens_delivery_id = int(delivery_itens_delivery_id)
            if not delivery_itens_weight:
                delivery_itens_weight = None
            else:
                delivery_itens_weight = float(delivery_itens_weight)

            if not delivery_itens_cubage:
                delivery_itens_cubage = None
            else:
                delivery_itens_cubage = float(delivery_itens_cubage)
        except ValueError:
            flash('Não foi possivel criar o item da entrega, somente numeros nos campos numericos', 'danger')
            return redirect(url_for('delivery_itens.update_delivery_itens', id=id))

        try:
            data.delivery_id = delivery_itens_delivery_id
            data.order_item_id = delivery_itens_order_item_id
            data.weight = delivery_itens_weight
            data.cubage = delivery_itens_cubage

            db.session.commit()
            flash('Item atualizado com sucesso', 'success')
            return redirect(url_for('delivery_itens.index'))
        except IntegrityError:
            flash('Erro ao Atualizar o item', 'danger')
            db.session.rollback()
            return redirect(url_for('delivery_itens.update_delivery_itens', id=id))


@delivery_itens_bp.route('/<int:id>/delete', methods=['POST'])
def delete_delivery_itens(id):
    data = db.session.get(DeliveryItem, id)
    if not data:
        flash('Não foi possivel localizar o item', 'danger')
        return redirect(url_for('delivery_itens.index'))
    try:
        db.session.delete(data)
        db.session.commit()
        flash('Item deletado com sucesso', 'success')
        return redirect(url_for('delivery_itens.index'))
    except IntegrityError:
        db.session.rollback()
        flash('Erro ao deletar o item', 'danger')
        return redirect(url_for('delivery_itens.index'))