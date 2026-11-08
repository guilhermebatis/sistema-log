from app.models.vehicle import Vehicle, FuelType, VehicleStatus
from service.vehicle_layer import create_vehicle, update_vehicle, delete_vehicle
from app import db


def test_vehivle_create(app):
    with app.test_request_context():

        vehicle = Vehicle(
        cargo_capacity_kg = 1000,
        cargo_capacity_m3 = 200,
        license_plate = 'TXQ-8956',
        model = 'MERCEDES',
        axle_count = 6,
        odometer = 10000,
        fuel_type = FuelType.DIESEL,
        )

        result = create_vehicle(vehicle)
        assert result == True


def test_vehivle_update(app):
    with app.test_request_context():

        vehicle = Vehicle(
        cargo_capacity_kg = 1000,
        cargo_capacity_m3 = 200,
        license_plate = 'TXQ-8956',
        model = 'MERCEDES',
        axle_count = 6,
        odometer = 10000,
        fuel_type = FuelType.DIESEL,
        )

        create_vehicle(vehicle)

        _var_update_vehicle = Vehicle(
        id = vehicle.id,
        cargo_capacity_kg = 2000,
        cargo_capacity_m3 = 400,
        license_plate = 'TQA-8563',
        status = VehicleStatus.AVAILABLE,
        model = 'SCANIA',
        axle_count = 8,
        odometer = 20000,
        fuel_type = FuelType.ELECTRIC,
        )

        result = update_vehicle(_var_update_vehicle)

        vehicle_test = db.session.query(Vehicle).filter(Vehicle.id == vehicle.id).one()

        assert result == True
        assert vehicle_test.id == 1
        assert vehicle_test.cargo_capacity_kg == 2000
        assert vehicle.cargo_capacity_m3 == 400
        assert vehicle.license_plate == 'TQA-8563'
        assert vehicle.status == VehicleStatus.AVAILABLE
        assert vehicle.model == 'SCANIA'
        assert vehicle.axle_count == 8
        assert vehicle.odometer == 20000
        assert vehicle.fuel_type == FuelType.ELECTRIC


def test_vehivle_update_nodata(app):
    with app.test_request_context():

        vehicle = Vehicle(
        cargo_capacity_kg = 1000,
        cargo_capacity_m3 = 200,
        license_plate = 'TXQ-8956',
        model = 'MERCEDES',
        axle_count = 6,
        odometer = 10000,
        fuel_type = FuelType.DIESEL,
        )

        create_vehicle(vehicle)

        _var_update_vehicle = Vehicle(
        id = 2,
        cargo_capacity_kg = 2000,
        cargo_capacity_m3 = 400,
        license_plate = 'TQA-8563',
        status = VehicleStatus.AVAILABLE,
        model = 'SCANIA',
        axle_count = 8,
        odometer = 20000,
        fuel_type = FuelType.ELECTRIC,
        )

        result = update_vehicle(_var_update_vehicle)

        assert result == False


def test_vehivle_delete(app):
    with app.test_request_context():
        vehicle = Vehicle(
            cargo_capacity_kg=1000,
            cargo_capacity_m3=200,
            license_plate='TXQ-8956',
            model='MERCEDES',
            axle_count=6,
            odometer=10000,
            fuel_type=FuelType.DIESEL,
        )

        create_vehicle(vehicle)


        result = delete_vehicle(vehicle)

        test_vehiche = db.session.query(Vehicle).filter(Vehicle.id == vehicle.id).one_or_none()

        assert result == True
        assert test_vehiche == None


def test_vehivle_delete_nodata(app):
    with app.test_request_context():
        vehicle = Vehicle(
            cargo_capacity_kg=1000,
            cargo_capacity_m3=200,
            license_plate='TXQ-8956',
            model='MERCEDES',
            axle_count=6,
            odometer=10000,
            fuel_type=FuelType.DIESEL,
        )

        vehicle_2 = Vehicle(
            cargo_capacity_kg=1000,
            cargo_capacity_m3=200,
            license_plate='TXQ-8956',
            model='MERCEDES',
            axle_count=6,
            odometer=10000,
            fuel_type=FuelType.DIESEL,
        )

        create_vehicle(vehicle)


        result = delete_vehicle(vehicle_2)

        test_vehiche = db.session.query(Vehicle).all()

        assert result == False
        assert len(test_vehiche) == 1


def test_vehivle_cargo_capacity_kg_none(app):
    with app.test_request_context():

        vehicle = Vehicle(
        cargo_capacity_kg = None,
        cargo_capacity_m3 = 200,
        license_plate = 'TXQ-8956',
        model = 'MERCEDES',
        axle_count = 6,
        odometer = 10000,
        fuel_type = FuelType.DIESEL,
        )

        result = create_vehicle(vehicle)
        assert result == False


def test_vehivle_cargo_capacity_kg_nonegative(app):
    with app.test_request_context():

        vehicle = Vehicle(
        cargo_capacity_kg = -1000,
        cargo_capacity_m3 = 200,
        license_plate = 'TXQ-8956',
        model = 'MERCEDES',
        axle_count = 6,
        odometer = 10000,
        fuel_type = FuelType.DIESEL,
        )

        result = create_vehicle(vehicle)
        assert result == False


def test_vehivle_cargo_capacity_m3_none(app):
    with app.test_request_context():

        vehicle = Vehicle(
        cargo_capacity_kg = 1000,
        cargo_capacity_m3 = None,
        license_plate = 'TXQ-8956',
        model = 'MERCEDES',
        axle_count = 6,
        odometer = 10000,
        fuel_type = FuelType.DIESEL,
        )

        result = create_vehicle(vehicle)
        assert result == False


def test_vehivle_cargo_capacity_m3_nonegative(app):
    with app.test_request_context():

        vehicle = Vehicle(
        cargo_capacity_kg = 1000,
        cargo_capacity_m3 = -200,
        license_plate = 'TXQ-8956',
        model = 'MERCEDES',
        axle_count = 6,
        odometer = 10000,
        fuel_type = FuelType.DIESEL,
        )

        result = create_vehicle(vehicle)
        assert result == False


def test_vehivle_license_plate_none(app):
    with app.test_request_context():

        vehicle = Vehicle(
        cargo_capacity_kg = 1000,
        cargo_capacity_m3 = 200,
        license_plate = None,
        model = 'MERCEDES',
        axle_count = 6,
        odometer = 10000,
        fuel_type = FuelType.DIESEL,
        )

        result = create_vehicle(vehicle)
        assert result == False


def test_vehivle_license_plate_unique(app):
    with app.test_request_context():

        vehicle = Vehicle(
        cargo_capacity_kg = 1000,
        cargo_capacity_m3 = 200,
        license_plate = 'TXQ-8956',
        model = 'MERCEDES',
        axle_count = 6,
        odometer = 10000,
        fuel_type = FuelType.DIESEL,
        )

        create_vehicle(vehicle)

        vehicle_2 = Vehicle(
        cargo_capacity_kg = 2000,
        cargo_capacity_m3 = 400,
        license_plate = 'TXQ-8956',
        model = 'Scania',
        axle_count = 8,
        odometer = 50000,
        fuel_type = FuelType.ELECTRIC,
        )

        result = create_vehicle(vehicle_2)

        assert result == False


def test_vehivle_model_none(app):
    with app.test_request_context():

        vehicle = Vehicle(
        cargo_capacity_kg = 1000,
        cargo_capacity_m3 = 200,
        license_plate = 'TXQ-8956',
        model = None,
        axle_count = 6,
        odometer = 10000,
        fuel_type = FuelType.DIESEL,
        )

        result = create_vehicle(vehicle)
        assert result == False


def test_vehivle_axle_count_none(app):
    with app.test_request_context():

        vehicle = Vehicle(
        cargo_capacity_kg = 1000,
        cargo_capacity_m3 = 200,
        license_plate = 'TXQ-8956',
        model = 'MERCEDES',
        axle_count = None,
        odometer = 10000,
        fuel_type = FuelType.DIESEL,
        )

        result = create_vehicle(vehicle)
        assert result == False


def test_vehivle_axle_count_nonegative(app):
    with app.test_request_context():

        vehicle = Vehicle(
        cargo_capacity_kg = 1000,
        cargo_capacity_m3 = 200,
        license_plate = 'TXQ-8956',
        model = 'MERCEDES',
        axle_count = -6,
        odometer = 10000,
        fuel_type = FuelType.DIESEL,
        )

        result = create_vehicle(vehicle)
        assert result == False


def test_vehivle_odometer_none(app):
    with app.test_request_context():

        vehicle = Vehicle(
        cargo_capacity_kg = 1000,
        cargo_capacity_m3 = 200,
        license_plate = 'TXQ-8956',
        model = 'MERCEDES',
        axle_count = 6,
        odometer = None,
        fuel_type = FuelType.DIESEL,
        )

        result = create_vehicle(vehicle)
        assert result == False


def test_vehivle_odometer_nonegative(app):
    with app.test_request_context():

        vehicle = Vehicle(
        cargo_capacity_kg = 1000,
        cargo_capacity_m3 = 200,
        license_plate = 'TXQ-8956',
        model = 'MERCEDES',
        axle_count = 6,
        odometer = -10000,
        fuel_type = FuelType.DIESEL,
        )

        result = create_vehicle(vehicle)
        assert result == False


def test_vehivle_update_license_plate_unique(app):
    with app.test_request_context():

        vehicle = Vehicle(
        cargo_capacity_kg = 1000,
        cargo_capacity_m3 = 200,
        license_plate = 'TXQ-8956',
        model = 'MERCEDES',
        axle_count = 6,
        odometer = 10000,
        fuel_type = FuelType.DIESEL,
        )

        vehicle_2 = Vehicle(
            cargo_capacity_kg=1000,
            cargo_capacity_m3=200,
            license_plate='QTH-5858',
            model='MERCEDES',
            axle_count=6,
            odometer=10000,
            fuel_type=FuelType.DIESEL,
        )

        create_vehicle(vehicle)
        create_vehicle(vehicle_2)


        _var_update_vehicle = Vehicle(
        id = vehicle.id,
        cargo_capacity_kg = 2000,
        cargo_capacity_m3 = 400,
        license_plate = 'QTH-5858',
        status = VehicleStatus.AVAILABLE,
        model = 'SCANIA',
        axle_count = 8,
        odometer = 20000,
        fuel_type = FuelType.ELECTRIC,
        )

        result = update_vehicle(_var_update_vehicle)

        assert result == False


def test_vehivle_fuel_type_none(app):
    with app.test_request_context():

        vehicle = Vehicle(
        cargo_capacity_kg = 1000,
        cargo_capacity_m3 = 200,
        license_plate = 'TXQ-8956',
        model = 'MERCEDES',
        axle_count = 6,
        odometer = 10000,
        fuel_type = None,
        )

        result = create_vehicle(vehicle)
        assert result == False