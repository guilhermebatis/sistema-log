from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.extensions import db
from app.models import Client
from service.client_layer import create_client_service, update_client_service, delete_client_service

client_bp = Blueprint('client', __name__, url_prefix='/client')

@client_bp.route('/create', methods=['GET', 'POST'])
def create_client():
    if request.method == 'POST':
        client_name = request.form.get('name', '').strip()
        client_cpf_cnpj = request.form.get('CPF_CNPJ', '').strip()
        client_email = request.form.get('email', '').strip()
        client_phone = request.form.get('phone', '').strip()

        new_client = Client(
            name = client_name,
            CPF_CNPJ = client_cpf_cnpj,
            email = client_email,
            phone = client_phone
        )

        if create_client_service(new_client):
            return redirect(url_for('client.client'))
        else:
            return render_template('clients/create.html')
    return render_template('clients/create.html')


@client_bp.route('/', methods=['GET'])
def client():
    data = db.session.query(Client).all()
    return render_template('clients/get.html', data=data)


@client_bp.route('/<int:id>/delete', methods=['POST'])
def client_delete(id):

    data = db.session.query(Client).filter(Client.id == id).one_or_none()

    if delete_client_service(data):
        return redirect(url_for('client.client'))
    else:
        return redirect(url_for('client.client'))


@client_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def client_update(id):
    if request.method == 'GET':
        data = db.session.get(Client, id)

        if not data:
            flash('cliente não foi encontrado!', 'danger')
            return redirect(url_for('client.client'))

        return render_template('clients/edit.html', data=data)

    if request.method == 'POST':
        data = db.session.get(Client, id)

        client_name = request.form.get('name', '').strip()
        client_cpf_cnpj = request.form.get('CPF_CNPJ', '').strip()
        client_email = request.form.get('email', '').strip()
        client_phone = request.form.get('phone', '').strip()

        data.name = client_name
        data.CPF_CNPJ = client_cpf_cnpj
        data.email = client_email
        data.phone = client_phone

        if update_client_service(data):
            return redirect(url_for('client.client'))
        else:
            return redirect(url_for('client.client_update', id=id))