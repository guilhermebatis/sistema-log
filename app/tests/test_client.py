from app.models import Client
from service.client_layer import create_client_service, update_client_service, delete_client_service
from app import db


def test_create_client_service(app):
    with app.test_request_context():

        client = Client(
        name = 'Client test',
        CPF_CNPJ = '123456789',
        email = 'Test@gmail.com',
        phone = '987654321',
        )

        result = create_client_service(client)
        assert result is True


def test_update_client(app):
    with app.test_request_context():

        client = Client(
        name = 'Client test',
        CPF_CNPJ = '123456789',
        email = 'Test@gmail.com',
        phone = '987654321',
        )

        create_client_service(client)

        client_up = Client(
            id = client.id,
            name = 'Test client',
            CPF_CNPJ = '987654321',
            email = 'TestUpdate@gmail.com',
            phone = '123456789',
        )

        result = update_client_service(client_up)

        client_test = db.session.query(Client).filter(Client.id == client_up.id).one()

        assert result is True
        assert client_test.name == 'Test client'
        assert client_test.CPF_CNPJ == '987654321'
        assert client_test.email == 'TestUpdate@gmail.com'
        assert client_test.phone == '123456789'


def test_delete_client(app):
    with app.test_request_context():
        client = Client(
            name='Client test',
            CPF_CNPJ='123456789',
            email='Test@gmail.com',
            phone='987654321',
        )

        create_client_service(client)

        result = delete_client_service(client)
        assert result is True

        client_test = db.session.query(Client).filter(Client.id == client.id).scalar()

        assert client_test is None


def test_client_name_none(app):
    with app.test_request_context():
        client = Client(
            name=None,
            CPF_CNPJ='123456789',
            email='Test@gmail.com',
            phone='987654321',
        )

        result = create_client_service(client)
        assert result is False


def test_client_CPF_CNPJ_none(app):
    with app.test_request_context():
        client = Client(
            name='Client test',
            CPF_CNPJ=None,
            email='Test@gmail.com',
            phone='987654321',
        )
        result = create_client_service(client)
        assert result is False


def test_client_phone_none(app):
    with app.test_request_context():
        client = Client(
            name='Client test',
            CPF_CNPJ='123456789',
            email='Test@gmail.com',
            phone=None,
        )
        result = create_client_service(client)
        assert result is False


def test_client_email_none(app):
    with app.test_request_context():
        client = Client(
            name='Client test',
            CPF_CNPJ='123456789',
            email=None,
            phone='987654321',
        )

        result = create_client_service(client)
        assert result is True


def test_client_CPF_CNPJ_unique(app):
    with app.test_request_context():
        client_1 = Client(
            name='Client test',
            CPF_CNPJ='123456789',
            email='Test@gmail.com',
            phone='987654321',
        )

        create_client_service(client_1)

        client_2 = Client(
            name='Client test 2',
            CPF_CNPJ='123456789',
            email='Test2@gmail.com',
            phone='98765432122',
        )

        result = create_client_service(client_2)
        assert result is False


def test_client_email_unique(app):
    with app.test_request_context():
        client_1 = Client(
            name='Client test',
            CPF_CNPJ='123456789',
            email='Test@gmail.com',
            phone='987654321',
        )

        create_client_service(client_1)

        client_2 = Client(
            name='Client test 2',
            CPF_CNPJ='12345678910',
            email='Test@gmail.com',
            phone='98765432122',
        )

        result = create_client_service(client_2)
        assert result is False


def test_client_email_unique_none(app):
    with app.test_request_context():
        client_1 = Client(
            name='Client test',
            CPF_CNPJ='123456789',
            email=None,
            phone='987654321',
        )

        create_client_service(client_1)

        client_2 = Client(
            name='Client test 2',
            CPF_CNPJ='12345678910',
            email=None,
            phone='98765432122',
        )

        result = create_client_service(client_2)
        assert result is True


def test_client_phone_unique(app):
    with app.test_request_context():
        client_1 = Client(
            name='Client test',
            CPF_CNPJ='123456789',
            email='Test@gmail.com',
            phone='987654321',
        )

        create_client_service(client_1)

        client_2 = Client(
            name='Client test 2',
            CPF_CNPJ='12345678910',
            email='Test@gmail.com',
            phone='98765432122',
        )

        result = create_client_service(client_2)
        assert result is False
    with app.test_request_context():
        client_1 = Client(
            name='Client test',
            CPF_CNPJ='123456789',
            email='Test@gmail.com',
            phone='987654321',
        )

        create_client_service(client_1)

        client_2 = Client(
            name='Client test 2',
            CPF_CNPJ='12345678910',
            email='Test2@gmail.com',
            phone='987654321',
        )

        result = create_client_service(client_2)
        assert result is False
