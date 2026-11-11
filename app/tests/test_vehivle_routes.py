from app import db
from app.models.vehicle import Vehicle, FuelType, VehicleStatus

def test_vehivle_get_routes(vehicle):
    with vehicle.application.app_context():
        response = vehicle.get('vehicle/')
        assert response.status_code == 200


def test_vehicle_create_routes(vehicle):
    with vehicle.application.app_context():

        vehicle_data = {
            'cargo_capacity_kg': 1000,
            'cargo_capacity_m3': 200,
            'license_plate': 'TGH-8563',
            'status': VehicleStatus.AVAILABLE.value,
            'model': 'SCANIA',
            'axle_count': 6,
            'odometer': 10000,
            'fuel_type': FuelType.DIESEL.value,
        }

        response = vehicle.post('/vehicle/create', data=vehicle_data)
        vehicle_exist = db.session.query(Vehicle).all()

        assert len(vehicle_exist) == 1
        assert response.status_code == 302


def test_vehivle_update_routes(vehicle):
    with vehicle.application.app_context():
        vehicle_data = {
            'id': 1,
            'cargo_capacity_kg': 1000,
            'cargo_capacity_m3': 200,
            'license_plate': 'TGH-8563',
            'status': VehicleStatus.AVAILABLE.value,
            'model': 'SCANIA',
            'axle_count': 6,
            'odometer': 10000,
            'fuel_type': FuelType.DIESEL.value,
        }

        vehicle_data_up = {
            'id': 1,
            'cargo_capacity_kg': 2000,
            'cargo_capacity_m3': 400,
            'license_plate': 'TGH-8563',
            'status': VehicleStatus.AVAILABLE.value,
            'model': 'SCANIA',
            'axle_count': 6,
            'odometer': 30000,
            'fuel_type': FuelType.DIESEL.value,
        }

        vehicle.post('/vehicle/create', data=vehicle_data)
        response = vehicle.post(f'/vehicle/{vehicle_data_up['id']}/update', data=vehicle_data_up)
        vehicle_exist = db.session.query(Vehicle).all()

        assert len(vehicle_exist) == 1
        assert response.status_code == 302
        assert vehicle_exist[0].cargo_capacity_kg == 2000


def test_vehicle_delete_route(vehicle):
    with vehicle.application.app_context():

        veicle_data = {
            'id': 1,
            'cargo_capacity_kg': 1000,
            'cargo_capacity_m3': 200,
            'license_plate': 'TGH-8563',
            'status': VehicleStatus.AVAILABLE.value,
            'model': 'SCANIA',
            'axle_count': 6,
            'odometer': 10000,
            'fuel_type': FuelType.DIESEL.value,
        }

        vehicle.post('/vehicle/create', data=veicle_data)
        response = vehicle.post(f'/vehicle/{veicle_data['id']}/delete')
        vehicle_exist = db.session.query(Vehicle).all()

        assert len(vehicle_exist) == 0
        assert response.status_code == 302