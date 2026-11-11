from sqlalchemy.exc import IntegrityError

from app.models import Vehicle
from flask import flash
from app import db


def _validate_vehicle(vehicle: Vehicle):

    if vehicle.cargo_capacity_kg is None:
        flash('O campo capacidade em KG de carga e obrigatorio', 'danger')
        return False
    if vehicle.cargo_capacity_kg <= 0:
        flash('A capacidade de carga em KG não pode ser menor que zero', 'danger')
        return False
    if vehicle.cargo_capacity_m3 is None:
        flash('O campo capacidade de carga em m3 e obrigatorio', 'danger')
        return False
    if vehicle.cargo_capacity_m3 <= 0:
        flash('A capacidade de carga em m3 não pode ser menor de zero', 'danger')
        return False
    if vehicle.license_plate is None:
        flash('O campo placa e obrigatorio', 'danger')
        return False
    if vehicle.model is None:
        flash('O campo modelo e obrigatorio', 'danger')
        return False
    if vehicle.axle_count is None:
        flash('O campo quantidade de eixos e obrigatorio', 'danger')
        return False
    if vehicle.axle_count <= 0:
        flash('A quantidade de eixos não pode ser menor que zero', 'danger')
        return False
    if vehicle.odometer is None:
        flash('O campo odometro e obrigatorio', 'danger')
        return False
    if vehicle.odometer <= 0:
        flash('O odometro não pode ser menor que zero', 'danger')
        return False
    if vehicle.fuel_type is None:
        flash('O campo tipo de combustivel e obrigadorio', 'danger')
        return False

    #Licence plate unique validation
    query = db.session.query(Vehicle).filter(Vehicle.license_plate == vehicle.license_plate)

    if vehicle.license_plate is not None:
        query = query.where(Vehicle.id != vehicle.id)

    validate_plate = db.session.execute(query).one_or_none()

    if validate_plate:
        flash('Placa do veiculo duplicado duplicado', 'danger')
        return False

    return True


def create_vehicle_service(vehicle: Vehicle):
    if not _validate_vehicle(vehicle):
        return False

    try:
        db.session.add(vehicle)
        db.session.commit()
        flash('Veiculo criado com sucesso', 'success')
        return True
    except IntegrityError:
        db.session.rollback()
        flash('Error ao criar veiculo', 'danger')
        return False


def update_vehicle_service(vehicle: Vehicle):
    data = db.session.query(Vehicle).filter(Vehicle.id == vehicle.id).one_or_none()

    if data is None:
        flash('Não foi possivel localizar o veiculo', 'danger')
        return False

    if not _validate_vehicle(vehicle):
        return False

    data.cargo_capacity_kg = vehicle.cargo_capacity_kg
    data.cargo_capacity_m3 = vehicle.cargo_capacity_m3
    data.license_plate = vehicle.license_plate
    data.status = vehicle.status
    data.model = vehicle.model
    data.axle_count = vehicle.axle_count
    data.odometer = vehicle.odometer
    data.fuel_type = vehicle.fuel_type


    try:
        db.session.add(data)
        db.session.commit()
        flash('Veiculo atualizado com sucesso', 'success')
        return True
    except IntegrityError as error:
        db.session.rollback()
        print(error)
        flash('Error ao atualizar veículo', 'danger')
        return False


def delete_vehicle_service(vehicle: Vehicle):
    data = db.session.query(Vehicle).filter(Vehicle.id == vehicle.id).one_or_none()

    if data is None:
        flash('Não foi possivel localizar o veiculo', 'danger')
        return False

    try:
        db.session.delete(vehicle)
        db.session.commit()
        flash('Veiculo removido com sucesso', 'success')
        return True
    except IntegrityError:
        db.session.rollback()
        flash('Error remover veiculo', 'danger')
        return False