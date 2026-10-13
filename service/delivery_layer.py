from sqlalchemy.exc import IntegrityError

from flask import flash
from app.models.delivery import StatusDelivery
from app.models import  DeliveryItem, Delivery
from app.models import OrderItem
from sqlalchemy import func, select
from app.extensions import db


def create_delivery_item(delivery_item: DeliveryItem):

    if not delivery_item.quantity or delivery_item.quantity <= 0:
        flash('Não foi possivel criar o item da entrega, a quantidade precisa ser positiva', 'danger')
        return False

    ordem_item_data = db.session.execute(
        select(
            OrderItem.quantity,
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
        StatusDelivery.FAILED
    ):
        flash('Não foi possivel criar o item da entrega,'
              ' a entrega ja foi concluida ou cancelada', 'danger')
        return False


    if delivery_data.order_service_id is None:
        flash('Não foi possivel criar o item da entrega, ordem de serviço não localizada', 'danger')
        return False

    if delivery_data.order_service_id != ordem_item_data.order_service_id:
        flash('Não foi possivel criar o item da entrega, a ordem de serviço e diferente', 'danger')
        return False

    quantity_delivery = db.session.scalar(
        select(
            (func.sum(DeliveryItem.quantity))
        .join(
                Delivery,
                DeliveryItem.delivery_id == Delivery.id)
        .where(
                DeliveryItem.order_item_id == delivery_item.order_item_id,
                Delivery.status.notin_([
                    StatusDelivery.CANCELLED,
                    StatusDelivery.FAILED
                ])
            )
        )
    )

    if quantity_delivery is None:
        quantity_delivery = 0

    if (delivery_item.quantity + quantity_delivery) > ordem_item_data.quantity:
        flash('A quantidade do item não pode ser maior do que a quantidade solicitada.', 'danger')
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

