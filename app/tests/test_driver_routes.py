from app.models.driver import DriverStatus, DrivingLicenceCategory, Driver
from app import db
import datetime


def test_driver_routes(driver):
    with driver.application.app_context():
        response = driver.get('driver/')
        assert response.status_code == 200


def test_driver_create_routes(driver):
    with driver.application.app_context():

        driver_data = {
            'name' : 'test_driver',
            'cnh': '123456789',
            'phone': '123456789',
            'admission_date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'licence_category': DrivingLicenceCategory.E.value,
            'license_expiration_date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'status': DriverStatus.AVAILABLE.value,
        }

        response = driver.post('/driver/create', data=driver_data)
        driver_exist = db.session.query(Driver).all()

        assert response.status_code == 302
        assert  len(driver_exist) == 1


def test_driver_update_routes(driver):
    with driver.application.app_context():

        driver_data_1 = {
            'id': 1,
            'name' : 'test_driver',
            'cnh': '123456789',
            'phone': '123456789',
            'admission_date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'licence_category': DrivingLicenceCategory.E.value,
            'license_expiration_date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'status': DriverStatus.AVAILABLE.value,
        }

        driver_data_2 = {
            'id': driver_data_1['id'],
            'name': 'test_driver_up',
            'cnh': '987654321',
            'phone': '987654321',
            'admission_date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'licence_category': DrivingLicenceCategory.A.value,
            'license_expiration_date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'status': DriverStatus.UNAVAILABLE.value,
        }

        driver.post('/driver/create', data=driver_data_1)
        response = driver.post(f'/driver/{driver_data_2['id']}/update', data=driver_data_2)
        driver_exist = db.session.query(Driver).first()

        assert response.status_code == 302
        assert  driver_exist.name == 'test_driver_up'


def test_driver_delete_routes(driver):
    with driver.application.app_context():
        driver_data = {
            'id': 1,
            'name': 'test_driver',
            'cnh': '123456789',
            'phone': '123456789',
            'admission_date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'licence_category': DrivingLicenceCategory.E.value,
            'license_expiration_date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'status': DriverStatus.AVAILABLE.value,
        }

        driver.post('/driver/create', data=driver_data)
        response = driver.post(f'/driver/{driver_data['id']}/delete', data=driver_data)

        driver_exist = db.session.query(Driver).all()

        assert response.status_code == 302
        assert len(driver_exist) == 0