import datetime
from app import db

from app.models.driver import DrivingLicenceCategory, DriverStatus, Driver
from service.driver_layer import create_driver, update_driver, delete_driver

def test_driver_create(app):
    with app.test_request_context():
        driver = Driver(
            name = 'test',
            cnh = '123456789',
            phone = '123456789',
            admission_date = datetime.datetime.now(),
            licence_category = DrivingLicenceCategory.E,
            license_expiration_date = datetime.datetime.now(),
            status = DriverStatus.AVAILABLE,
        )

        result = create_driver(driver)
        assert result == True


def test_driver_update(app):
    with app.test_request_context():
        driver = Driver(
            name = 'test',
            cnh = '123456789',
            phone = '123456789',
            admission_date = datetime.datetime.now(),
            licence_category = DrivingLicenceCategory.E,
            license_expiration_date = datetime.datetime.now(),
            status = DriverStatus.AVAILABLE,
        )

        create_driver(driver)

        var_driver_update = Driver(
            id = driver.id,
            name = 'test1',
            cnh = '987654321',
            phone = '987654321',
            admission_date = datetime.datetime.now(),
            licence_category = DrivingLicenceCategory.A,
            license_expiration_date = datetime.datetime.now(),
            status = DriverStatus.UNAVAILABLE,
        )

        result = update_driver(var_driver_update)

        driver_db = db.session.query(Driver).filter(Driver.id == driver.id).all()

        assert result == True
        assert driver_db[0].name == var_driver_update.name
        assert len(driver_db) == 1
        assert driver_db[0].name != 'test'


def test_driver_delete(app):
    with app.test_request_context():
        driver = Driver(
            name='test',
            cnh='123456789',
            phone='123456789',
            admission_date=datetime.datetime.now(),
            licence_category=DrivingLicenceCategory.E,
            license_expiration_date=datetime.datetime.now(),
            status=DriverStatus.AVAILABLE,
        )

        create_driver(driver)

        result = delete_driver(driver)

        driver_db = db.session.query(Driver).filter(Driver.id == driver.id).all()

        assert result == True
        assert len(driver_db) == 0


def test_driver_name_none(app):
    with app.test_request_context():
        driver = Driver(
            name = None,
            cnh = '123456789',
            phone = '123456789',
            admission_date = datetime.datetime.now(),
            licence_category = DrivingLicenceCategory.E,
            license_expiration_date = datetime.datetime.now(),
            status = DriverStatus.AVAILABLE,
        )

        result = create_driver(driver)
        assert result == False


def test_driver_cnh_none(app):
    with app.test_request_context():
        driver = Driver(
            name = 'test',
            cnh = None,
            phone = '123456789',
            admission_date = datetime.datetime.now(),
            licence_category = DrivingLicenceCategory.E,
            license_expiration_date = datetime.datetime.now(),
            status = DriverStatus.AVAILABLE,
        )

        result = create_driver(driver)
        assert result == False


def test_driver_phone_none(app):
    with app.test_request_context():
        driver = Driver(
            name = 'test',
            cnh = '123456789',
            phone = None,
            admission_date = datetime.datetime.now(),
            licence_category = DrivingLicenceCategory.E,
            license_expiration_date = datetime.datetime.now(),
            status = DriverStatus.AVAILABLE,
        )

        result = create_driver(driver)
        assert result == False


def test_driver_licence_category_none(app):
    with app.test_request_context():
        driver = Driver(
            name = 'test',
            cnh = '123456789',
            phone = '123456789',
            admission_date = datetime.datetime.now(),
            licence_category = None,
            license_expiration_date = datetime.datetime.now(),
            status = DriverStatus.AVAILABLE,
        )

        result = create_driver(driver)
        assert result == False


def test_driver_cnh_unique(app):
    with app.test_request_context():
        driver = Driver(
            name = 'test',
            cnh = '123456789',
            phone = '123456789',
            admission_date = datetime.datetime.now(),
            licence_category = DrivingLicenceCategory.E,
            license_expiration_date = datetime.datetime.now(),
            status = DriverStatus.AVAILABLE,
        )

        driver2 = Driver(
            name='test2',
            cnh='123456789',
            phone='123456789',
            admission_date=datetime.datetime.now(),
            licence_category=DrivingLicenceCategory.E,
            license_expiration_date=datetime.datetime.now(),
            status=DriverStatus.AVAILABLE,
        )

        create_driver(driver)
        result = create_driver(driver2)
        assert result == False


def test_driver_updata_cnh_unique(app):
    with app.test_request_context():
        driver = Driver(
            name = 'test',
            cnh = '123456789',
            phone = '123456789',
            admission_date = datetime.datetime.now(),
            licence_category = DrivingLicenceCategory.E,
            license_expiration_date = datetime.datetime.now(),
            status = DriverStatus.AVAILABLE,
        )

        driver2 = Driver(
            name='test2',
            cnh='987654321',
            phone='123456789',
            admission_date=datetime.datetime.now(),
            licence_category=DrivingLicenceCategory.E,
            license_expiration_date=datetime.datetime.now(),
            status=DriverStatus.AVAILABLE,
        )

        driver_update = Driver(
            id = driver.id,
            name = 'test',
            cnh = '987654321',
            phone = '123456789',
            admission_date = datetime.datetime.now(),
            licence_category = DrivingLicenceCategory.E,
            license_expiration_date = datetime.datetime.now(),
            status = DriverStatus.AVAILABLE,
        )


        create_driver(driver)
        create_driver(driver2)
        result = update_driver(driver_update)
        assert result == False