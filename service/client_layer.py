from sqlalchemy import or_

from sqlalchemy.exc import IntegrityError

from flask import flash
from app.models import Client
from app.extensions import db



def _validate_client(client: Client):
    if client.name is None:
        flash('Não foi possivel criar o cliente, precisa de um nome valido', 'danger')
        return False
    if client.CPF_CNPJ is None:
        flash('Não foi possivel criar o cliente, precisa do CPF valido', 'danger')
        return False
    if client.phone is None:
        flash('Não foi possivel criar o cliente, precisa do telefone', 'danger')
        return False

    conditions = [
        Client.CPF_CNPJ == client.CPF_CNPJ
    ]

    if client.email:
        conditions.append(Client.email == client.email)

    if client.phone:
        conditions.append(Client.phone == client.phone)

    query = (db.select(
        Client.CPF_CNPJ,
        Client.email,
        Client.phone,
    )
    .where(or_(*conditions)))

    if client.id is not None:
        query = query.where(Client.id != client.id)

    results = db.session.execute(query).all()

    for item in results:
        if client.email is not None:
            if item.email == client.email:
                flash('Email duplicado', 'danger')
                return False
        if item.phone == client.phone:
            flash('Telefone duplicado', 'danger')
            return False
        if item.CPF_CNPJ == client.CPF_CNPJ:
            flash('CPF duplicado', 'danger')
            return False

    return True


def create_client_service(client: Client):

    if not _validate_client(client):
        return False

    try:
        db.session.add(client)
        db.session.commit()
        flash('Cliente criado com sucesso', 'success')
        return True
    except IntegrityError:
        db.session.rollback()
        flash('Erro ao criar cliente', 'danger')
        return False


def update_client_service(client: Client):
    if not _validate_client(client):
        return False

    data = db.session.get(Client, client.id)

    if not data:
        flash('Não foi possivel localizar o cliente', 'danger')
        return False

    data.name = client.name
    data.CPF_CNPJ = client.CPF_CNPJ
    data.email = client.email
    data.phone = client.phone

    try:
        db.session.add(data)
        db.session.commit()
        flash('Cliente atualizado com sucesso', 'success')
        return True
    except IntegrityError:
        db.session.rollback()
        flash('Erro ao atualizar cliente', 'danger')
        return False


def delete_client_service(client: Client):

    data = db.session.get(Client, client.id)

    if not data:
        flash('Não foi possivel localizar o cliente', 'danger')
        return False

    try:
        db.session.delete(data)
        db.session.commit()
        flash('Cliente deletado com sucesso', 'success')
        return True
    except IntegrityError:
        db.session.rollback()
        flash('Erro ao atualizar cliente', 'danger')
        return False


