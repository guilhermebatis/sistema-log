from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.extensions import db
from app.models import Vehicle
from app.models.vehicle import FuelType, VehicleStatus
from service.vehicle_layer import create_vehicle_service, update_vehicle_service, delete_vehicle_service
from flask_login import login_required


vehicle_bp = Blueprint('vehicle', __name__, url_prefix='/vehicle')


@vehicle_bp.route('/', methods=['GET'])
@login_required
def index():
    data = db.session.query(Vehicle).all()
    return render_template('vehicle/index.html', data=data)


@vehicle_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_vehicle():
    if request.method == 'POST':

        #recive data from form
        cargo_capacity_kg = request.form.get('cargo_capacity_kg', '').strip()
        cargo_capacity_m3 = request.form.get('cargo_capacity_m3', '').strip()
        license_plate = request.form.get('license_plate', '').strip()
        status = request.form.get('status', VehicleStatus.AVAILABLE)
        model = request.form.get('model', '').strip()
        axle_count = request.form.get('axle_count', '').strip()
        odometer = request.form.get('odometer', '').strip()
        fuel_type = request.form.get('fuel_type', FuelType.DIESEL)

        # data tranformation
        try:
            cargo_capacity_kg = int(cargo_capacity_kg)
            cargo_capacity_m3 = float(cargo_capacity_m3)
            axle_count = int(axle_count)
            odometer = int(odometer)
            status = VehicleStatus(status)
            fuel_type = FuelType(fuel_type)
        except ValueError:
            flash('Não foi possivel cadastrar o veiculo.', 'danger')
            return redirect(url_for('vehicle.create_vehicle'))

        #Create vehicle in database
        new_vehicle = Vehicle(
        cargo_capacity_kg = cargo_capacity_kg,
        cargo_capacity_m3 = cargo_capacity_m3,
        license_plate = license_plate,
        status = status,
        model = model,
        axle_count = axle_count,
        odometer = odometer,
        fuel_type = fuel_type,
        )

        if create_vehicle_service(new_vehicle):
            return redirect(url_for('vehicle.index'))
        else:
            return redirect(url_for('vehicle.create_vehicle'))

    return render_template('vehicle/create.html')


@vehicle_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_vehicle(id):

    data = db.session.get(Vehicle, id)

    if not data:
        return redirect(url_for('vehicle.index'))

    if delete_vehicle_service(data):
        return redirect(url_for('vehicle.index'))
    else:
        return redirect(url_for('vehicle.index'))


@vehicle_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_vehicle(id):
    if request.method == 'GET':
        data = db.session.get(Vehicle, id)
        if not data:
            flash('Veiculo não encontrado', 'danger')
            return redirect(url_for('vehicle.index'))
        return render_template('vehicle/update.html', data=data)

    if request.method == 'POST':
        data = db.session.get(Vehicle, id)

        if not data:
            flash('Veiculo não encontrado', 'danger')
            return redirect(url_for('vehicle.update_vehicle', id=id))

        #recive data from form
        vehicle_cargo_capacity_kg = request.form.get('cargo_capacity_kg', '').strip()
        vehicle_cargo_capacity_m3 = request.form.get('cargo_capacity_m3', '').strip()
        vehicle_license_plate = request.form.get('license_plate', '').strip()
        vehicle_status = request.form.get('status', '').strip()
        vehicle_model = request.form.get('model', '').strip()
        vehicle_axle_count = request.form.get('axle_count', '').strip()
        vehicle_odometer = request.form.get('odometer', '').strip()
        vehicle_fuel_type = request.form.get('fuel_type', '').strip()

        # data tranformation

        try:
            vehicle_cargo_capacity_kg = int(vehicle_cargo_capacity_kg)
            vehicle_cargo_capacity_m3 = float(vehicle_cargo_capacity_m3)
            vehicle_status = VehicleStatus(vehicle_status)
            vehicle_axle_count= int(vehicle_axle_count)
            vehicle_odometer = int(vehicle_odometer)
            vehicle_fuel_type = FuelType(vehicle_fuel_type)
        except ValueError:
            flash('Não foi possivel atualiar o veiculo', 'danger')
            return redirect(url_for('vehicle.update_vehicle', id=id))

        # Update data
        data.cargo_capacity_kg = vehicle_cargo_capacity_kg
        data.cargo_capacity_m3 = vehicle_cargo_capacity_m3
        data.status = vehicle_status
        data.axle_count = vehicle_axle_count
        data.odometer = vehicle_odometer
        data.fuel_type = vehicle_fuel_type
        data.license_plate = vehicle_license_plate
        data.model = vehicle_model

        if update_vehicle_service(data):
            return redirect(url_for('vehicle.index'))
        else:
            return redirect(url_for('vehicle.update_vehicle', id=id))