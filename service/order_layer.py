from app.models import OrderItem, OrderService
from sqlalchemy.exc import IntegrityError

from flask import flash
from app.extensions import db


def _validade_order_item(order_item: OrderItem):
    if not order_item.order_service_id:
        flash('Precisa do campo ordem de serviço', 'danger')
        return False
    if not order_item.quantity or order_item.quantity < 0:
        flash('A quantidade deve ser positiva', 'danger')
        return False
    if not order_item.weight or order_item.weight < 0:
        flash('O peso deve ser positivo', 'danger')
        return False
    if not order_item.cubage or order_item.cubage < 0:
        flash('A cubagem deve ser positiva', 'danger')
        return False
    if not order_item.price_item or order_item.price_item < 0:
        flash('O preço do item deve ser positivo', 'danger')
        return False
    return True


def create_order_item(order_item: OrderItem):
    if not _validade_order_item(order_item):
        return False

    try:
        db.session.add(order_item)
        db.session.commit()
        flash('O item foi criado com sucesso', 'success')
        return True
    except IntegrityError:
        db.session.rollback()
        flash('Erro ao criar o item', 'danger')
        return False


def update_order_item(order_item: OrderItem):
    if not _validade_order_item(order_item):
        return False

    data = db.session.get(OrderItem, order_item.id)
    if not data:
        flash('Não foi possivel localizar o item da entrega', 'danger')
        return

    data.order_service_id = order_item.order_service_id
    data.quantity = order_item.quantity
    data.description = order_item.description
    data.weight = order_item.weight
    data.cubage = order_item.cubage
    data.price_item = order_item.price_item

    try:
        db.session.add(data)
        db.session.commit()
        flash('Item atualizado com sucesso', 'success')
        return True
    except IntegrityError:
        db.session.rollback()
        flash('Erro ao atualizar o item', 'danger')
        return False


def delete_order_item(order_item: OrderItem):
    data = db.session.get(OrderItem, order_item.id)

    try:
        db.session.delete(data)
        db.session.commit()
        flash('Item deletado com sucesso', 'success')
        return True
    except IntegrityError:
        flash('Erro ao deletar o item', 'danger')
        return False


def _validate_order_service(order_service: OrderService):
    if order_service.weight_total < 0:
        flash('O peso total deve ser positivo', 'danger')
        return False
    if order_service.cubage_total < 0:
        flash('O cubagem total deve ser positivo', 'danger')
        return False
    if not order_service.origin or not order_service.destination:
        flash('O campo origem e destino precisam ser preencidos', 'danger')
        return False
    if not order_service.distance or order_service.distance < 0:
        flash('A distançia precisa ser positiva', 'danger')
        return False
    if order_service.price < 0:
        flash('O preço precisa ser positivo', 'danger')
        return False
    if not order_service.status:
        flash('O status precisa ser preenchido', 'danger')
        return False
    return True


def create_order_service(order_service: OrderService):
    if not _validate_order_service(order_service):
        return False

    try:
        db.session.add(order_service)
        db.session.commit()
        flash('A ordem de serviço foi criado com sucesso', 'success')
        return True
    except IntegrityError:
        db.session.rollback()
        flash('Erro ao criar a ordem de serviço', 'danger')
        return False

def update_order_service(order_service: OrderService):

    data = db.session.get(OrderService, order_service.id)

    if not data:
        flash('Não foi possivel localizar a ordem de serviço', 'danger')
        return False

    data.client_id = order_service.client_id
    data.weight_total = order_service.weight_total
    data.cubage_total = order_service.cubage_total
    data.origin = order_service.origin
    data.destination = order_service.destination
    data.distance = order_service.distance
    data.status = order_service.status
    data.price = order_service.price

    try:
        db.session.add(data)
        db.session.commit()
        flash('Ordem de serviço atualizado com sucesso', 'success')
        return True
    except IntegrityError:
        db.session.rollback()
        flash('Erro ao atualizar a ordem de serviço', 'danger')
        return False


def delete_order_service(order_service: OrderService):

    data = db.session.get(OrderService, order_service.id)

    if not data:
        flash('Não foi possivel localizar a odem de serciço', 'danger')
        return False

    try:
        db.session.delete(data)
        db.session.commit()
        flash('Ordem de serviço deletada com sucesso', 'success')
        return True
    except IntegrityError:
        db.session.rollback()
        flash('Error ao deletar a ordem de serviço', 'danger')
        return False



