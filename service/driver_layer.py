from pygments.lexers import q
from sqlalchemy.exc import IntegrityError

from app.models import Driver
from flask import flash
from app import db


def _validate_driver(driver: Driver):
    if driver.name is None:
        flash('O campo motorista e obrigatorio', 'danger')
        return False
    if driver.cnh is None:
        flash('O campo cnh e obrigatorio', 'danger')
        return False
    if driver.phone is None:
        flash('O campo telefone e obrigatorio', 'danger')
        return False
    if driver.licence_category is None:
        flash('O campo categoria da licena e obrigatorio', 'danger')
        return False

    #cnh unique validation

    query = db.session.query(Driver).filter(Driver.cnh == driver.cnh)

    if driver.id is not None:
        query = query.filter(Driver.id != driver.id)

    validate_cnh = db.session.execute(query).one_or_none()

    if validate_cnh:
        flash('A cnh esta duplicada', 'danger')
        return False
    return True


def create_driver(driver: Driver):
    if not _validate_driver(driver):
        return False

    try:
        db.session.add(driver)
        db.session.commit()
        flash('Morotista criado com sucesso', 'success')
        return True
    except IntegrityError:
        db.session.rollback()
        flash('Error ao criar o Morotista', 'danger')


def update_driver(driver: Driver):
    data = db.session.query(Driver).filter(Driver.id == driver.id).one_or_none()

    if data is None:
        flash('Motorista não encontrado', 'danger')
        return False

    if not _validate_driver(driver):
        return False

    data.name = driver.name
    data.cnh = driver.cnh
    data.phone = driver.phone
    data.admission_date = driver.admission_date
    data.licence_category = driver.licence_category
    data.license_expiration_date = driver.license_expiration_date
    data.status = driver.status

    try:
        db.session.commit()
        flash('Motorista atualizado com sucesso', 'success')
        return True
    except IntegrityError:
        db.session.rollback()
        flash('Error ao atualizar o Motorista', 'danger')
        return False


def delete_driver(driver: Driver):
    data = db.session.query(Driver).filter(Driver.id == driver.id).one_or_none()
    if data is None:
        flash('Motorista não encontrado', 'danger')
        return False

    try:
        db.session.delete(driver)
        db.session.commit()
        flash('Motorista deletado com sucesso', 'success')
        return True
    except IntegrityError:
        db.session.rollback()
        flash('Error ao deletar o Motorista', 'danger')
        return False