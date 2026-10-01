from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.order_service import OrderService, OrderItem

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


        if not order_item_order_service_id:
            flash('Não foi possivel criar a ordem de serviço, falta o campo cliente', 'danger')
            return redirect(url_for('order_items.create_order_item'))
        if not order_item_quantity:
            flash('Não foi possivel criar a ordem de serviço, falta o campo quantidade', 'danger')
            return redirect(url_for('order_items.create_order_item'))
        if not order_item_weight:
            flash('Não foi possivel criar a ordem de serviço, falta o campo peso', 'danger')
            return redirect(url_for('order_items.create_order_item'))
        if not order_item_cubage:
            flash('Não foi possivel criar a ordem de serviço, falta o campo cubagem', 'danger')
            return redirect(url_for('order_items.create_order_item'))
        if not order_item_price_item:
            flash('Não foi possivel criar a ordem de serviço, falta o campo preço do item', 'danger')
            return redirect(url_for('order_items.create_order_item'))

        try:
            order_item_order_service_id = int(order_item_order_service_id)
            order_item_quantity = int(order_item_quantity)
            order_item_weight = float(order_item_weight)
            order_item_cubage = float(order_item_cubage)
            order_item_price_item = float(order_item_price_item)
        except ValueError:
            flash('')
            return redirect(url_for('order_items.create_order_item'))

        if (order_item_quantity < 0
            or order_item_weight <0
            or order_item_cubage <0
            or order_item_price_item < 0):
            flash('Não foi possivel criar a ordem de serviço, so pode ter numeros positivos', 'danger')
            return redirect(url_for('order_items.create_order_item'))

        try:
            new_order_item = OrderItem(
                order_service_id = order_item_order_service_id,
                quantity = order_item_quantity,
                description = order_item_description,
                weight = order_item_weight,
                cubage = order_item_cubage,
                price_item = order_item_price_item,
            )

            db.session.add(new_order_item)
            db.session.commit()
            flash('Item da ordem criado com sucesso', 'success')
            return redirect(url_for('order_items.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Nao foi possivel criar a ordem de serviço')
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


        if not order_item_order_service_id:
            flash('Não foi possivel criar a ordem de serviço, falta o campo cliente', 'danger')
            return redirect(url_for('order_items.update_order_item', order_item_id=order_item_id))
        if not order_item_quantity:
            flash('Não foi possivel criar a ordem de serviço, falta o campo quantidade', 'danger')
            return redirect(url_for('order_items.update_order_item', order_item_id=order_item_id))
        if not order_item_weight:
            flash('Não foi possivel criar a ordem de serviço, falta o campo peso', 'danger')
            return redirect(url_for('order_items.update_order_item', order_item_id=order_item_id))
        if not order_item_cubage:
            flash('Não foi possivel criar a ordem de serviço, falta o campo cubagem', 'danger')
            return redirect(url_for('order_items.update_order_item', order_item_id=order_item_id))
        if not order_item_price_item:
            flash('Não foi possivel criar a ordem de serviço, falta o campo preço do item', 'danger')
            return redirect(url_for('order_items.update_order_item', order_item_id=order_item_id))

        try:
            order_item_order_service_id = int(order_item_order_service_id)
            order_item_quantity = int(order_item_quantity)
            order_item_weight = float(order_item_weight)
            order_item_cubage = float(order_item_cubage)
            order_item_price_item = float(order_item_price_item)
        except ValueError:
            flash('Não foi possivel atualizar o item da ordem', 'danger')
            return redirect(url_for('order_items.update_order_item', order_item_id=order_item_id))

        if (order_item_quantity < 0
            or order_item_weight <0
            or order_item_cubage <0
            or order_item_price_item < 0):
            flash('Não foi possivel criar a ordem de serviço, so pode ter numeros positivos', 'danger')
            return redirect(url_for('order_items.update_order_item', order_item_id=order_item_id))

        try:
            data.order_service_id = order_item_order_service_id
            data.quantity = order_item_quantity
            data.description = order_item_description
            data.weight = order_item_weight
            data.cubage = order_item_cubage
            data.price_item = order_item_price_item

            db.session.commit()
            flash('Item da order atualizado com sucesso', 'success')
            return redirect(url_for('order_items.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Error ao atualizar o item da order', 'danger')
            return redirect(url_for('order_items.update_order_item', order_item_id=order_item_id))


@order_items_bp.route("/<int:order_item_id>/delete", methods=['POST'])
def delete_order_item(order_item_id):
    data = db.session.get(OrderItem, order_item_id)

    if not data:
        flash('Não foi possivel localizar o item da ordem', 'danger')
        return redirect(url_for('order_items.index'))

    try:
        db.session.delete(data)
        db.session.commit()
        flash('Item deletado com sucesso', 'success')
        return redirect(url_for('order_items.index'))
    except IntegrityError:
        db.session.rollback()
        flash('Error ao deletar o item da ordem', 'danger')
        return redirect(url_for('order_items.index'))
