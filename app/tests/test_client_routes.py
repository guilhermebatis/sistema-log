from app.models import Client

def test_client_routes(client):
    response = client.get('client/')
    assert response.status_code == 200


def test_client_routes_create_client(client):
    data = {
        'client_name': 'test1',
        'client_cpf_cnpj': '123456789',
        'client_email': 'test@gmail.com',
        'client_phone': '123456789',
    }

    response = client.post('client/create', data=data)
    assert response.status_code == 302


def test_client_routes_update_client(client, app):
    with app.app_context():
        data = {
            'name': 'test1',
            'cpf_cnpj': '123456789',
            'email': 'test@gmail.com',
            'phone': '123456789',
        }
        response = client.post('client/create', data=data)
        assert response.status_code == 302

        data2 = {
            'id': 1,
            'name': 'test2',
            'cpf_cnpj': '987654321',
            'email': 'test@gmail.com',
            'phone': '987654321',
        }

        client_exist = Client.query.filter_by(name='test1').first()

        response = client.post(f'client/{client_exist.id}/update', data=data2)
        assert response.status_code == 302


def test_client_routes_delete_client(client, app):
    with app.app_context():
        data = {
            'name': 'test1',
            'cpf_cnpj': '123456789',
            'email': 'test@gmail.com',
            'phone': '123456789',
        }
        response = client.post('client/create', data=data)
        assert response.status_code == 302

        client_exist = Client.query.filter_by(name='test1').first()

        response = client.post(f'client/{client_exist.id}/delete', data=data)
        assert response.status_code == 302

        client_exist = Client.query.filter_by(name='test1').first()
        assert client_exist is None