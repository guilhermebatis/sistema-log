from sqlalchemy.exc import IntegrityError

from flask import flash
from app.models.delivery import StatusDelivery
from app.models import  DeliveryItem, Delivery
from app.models import OrderItem
from sqlalchemy import func, select
from app.extensions import db


def _validate_delivery_item(delivery_item: DeliveryItem):
    if delivery_item.order_item_id is None:
        flash('Não foi possivel criar o item da entrega, a precisa do item', 'danger')
        return False
    if delivery_item.delivery_id is None:
        flash('Não foi possivel criar o item da entrega, a precisa da entrega', 'danger')
        return False
    if not delivery_item.quantity or delivery_item.quantity <= 0:
        flash('Não foi possivel criar o item da entrega, a quantidade precisa ser positiva', 'danger')
        return False
    if not delivery_item.cubage or delivery_item.cubage <= 0:
        flash('Não foi possivel criar o item da entrega, a cubagem precisa ser positiva', 'danger')
        return False
    if not delivery_item.weight or delivery_item.weight <= 0:
        flash('Não foi possivel criar o item da entrega, o peso precisa ser positiva', 'danger')
        return False
    return True


def _validate_delivery_item_relations_and_limits(delivery_item: DeliveryItem):
    ordem_item_data = db.session.execute(
        select(
            OrderItem.quantity,
            OrderItem.weight,
            OrderItem.cubage,
            OrderItem.order_service_id,
        ).where(
            OrderItem.id == delivery_item.order_item_id
        )
    ).one_or_none()

    if ordem_item_data is None:
        flash('Item do pedido não encontrado', 'danger')
        return False

    delivery_data = db.session.execute(
        select(Delivery.status,
               Delivery.order_service_id)
        .where(Delivery.id == delivery_item.delivery_id)
    ).one_or_none()

    if delivery_data is None:
        flash('Não foi possivel criar o item da entrega, Entrega não localizada', 'danger')
        return False

    if delivery_data.status in (
            StatusDelivery.CANCELLED,
            StatusDelivery.COMPLETED,
            StatusDelivery.FAILED,
    ):
        flash('Não foi possivel criar o item da entrega,'
              ' a entrega ja foi concluida ou cancelada', 'danger')
        return False

    if delivery_data.order_service_id != ordem_item_data.order_service_id:
        flash('Não foi possivel criar o item da entrega, a ordem de serviço e diferente', 'danger')
        return False

    query = (select(
            func.coalesce(func.sum(DeliveryItem.quantity), 0).label('quantity'),
            func.coalesce(func.sum(DeliveryItem.cubage), 0).label('cubage'),
            func.coalesce(func.sum(DeliveryItem.weight), 0).label('weight'),
        )
        .join(
            Delivery,
            Delivery.id == DeliveryItem.delivery_id,
        )
        .where(
            DeliveryItem.order_item_id == delivery_item.order_item_id,
            Delivery.status.notin_([
                StatusDelivery.CANCELLED,
                StatusDelivery.FAILED,
            ])
        ))

    if delivery_item.id is not None:
        query = query.where(
            DeliveryItem.id != delivery_item.id
        )

    total_item_delivery_data = db.session.execute(query).one()


    if (delivery_item.quantity + total_item_delivery_data.quantity) > ordem_item_data.quantity:
        flash('A quantidade do item não pode ser maior do que a quantidade solicitada.', 'danger')
        return False

    if (delivery_item.weight + total_item_delivery_data.weight) > ordem_item_data.weight:
        flash('O peso do item não pode ser maior do que a peso solicitada.', 'danger')
        return False

    if (delivery_item.cubage + total_item_delivery_data.cubage) > ordem_item_data.cubage:
        flash('A cubagem do item não pode ser maior do que a cubagem solicitada.', 'danger')
        return False

    return True


def create_delivery_item(delivery_item: DeliveryItem):

    if not _validate_delivery_item(delivery_item):
        return False

    if not _validate_delivery_item_relations_and_limits(delivery_item):
        return False

    try:
        db.session.add(delivery_item)
        db.session.commit()
        flash('Item da entrega criado com sucesso', 'success')
        return True
    except IntegrityError:
        db.session.rollback()
        flash('Error ao criar o item da entrega', 'danger')
        return False


def update_delivery_item(delivery_item: DeliveryItem):

    data = db.session.get(DeliveryItem, delivery_item.id)

    if not data:
        flash('Erro ao localizar o item da entrega', 'danger')
        return False

    if not _validate_delivery_item(delivery_item):
        return False

    if not _validate_delivery_item_relations_and_limits(delivery_item):
        return False

    data.order_item_id = delivery_item.order_item_id
    data.delivery_id = delivery_item.delivery_id
    data.weight = delivery_item.weight
    data.quantity = delivery_item.quantity
    data.cubage = delivery_item.cubage

    try:
        db.session.commit()
        flash('Item da entrega atualizado com sucesso', 'success')
        return True
    except IntegrityError:
        db.session.rollback()
        flash('Error ao atualizar o item da entrega', 'danger')
        return False


def delete_delivery_item(delivery_item: DeliveryItem):

    data = db.session.get(DeliveryItem, delivery_item.id)
    if not data:
        flash('Erro ao localizar o item da entrega', 'danger')
        return False

    try:
        db.session.delete(data)
        db.session.commit()
        flash('Item da entrega deletado com sucesso', 'success')
        return True
    except IntegrityError:
        db.session.rollback()
        flash('Error ao deletar o item da entrega', 'danger')
        return False
