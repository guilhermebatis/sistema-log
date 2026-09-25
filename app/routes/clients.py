from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Client

client_bp = Blueprint('client', __name__, url_prefix='/client')

@client_bp.route('/create', methods=['GET', 'POST'])
def create_client():
    if request.method == 'POST':
        client_name = request.form.get('name', '').strip()
        client_cpf_cnpj = request.form.get('CPF_CNPJ', '').strip()
        client_email = request.form.get('email', '').strip()
        client_phone = request.form.get('phone', '').strip()

        if not client_name:
            flash('Não foi possível cadastrar o cliente, falta o campo nome.', 'danger')
            return redirect(url_for('client.create_client'))

        if not client_cpf_cnpj:
            flash('Não foi possível cadastrar o cliente, falta o campo cpf_cnpj.', 'danger')
            return redirect(url_for('client.create_client'))

        if not client_phone:
            flash('Não foi possível cadastrar o cliente, falta o campo telefone.', 'danger')
            return redirect(url_for('client.create_client'))


        new_client = Client(
            name = client_name,
            CPF_CNPJ = client_cpf_cnpj,
            email = client_email,
            phone = client_phone
        )

        db.session.add(new_client)

        try:
            db.session.commit()
            flash('Cliente criado com sucesso!', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Não foi possível cadastrar o cliente.', 'danger')

        return redirect(url_for('client.create_client'))

    return render_template('clients/create.html')


@client_bp.route('/', methods=['GET'])
def client():
    data = db.session.query(Client).all()
    return render_template('clients/get.html', data=data)


@client_bp.route('/<int:id>/delete', methods=['POST'])
def client_delete(id):
    try:
        data = db.session.get(Client, id)

        if not data:
            flash('cliente não foi encontrado!', 'danger')
            return redirect(url_for('client.client'))

        db.session.delete(data)
        db.session.commit()
        flash('Cliente deletado com sucesso!', 'success')
        return redirect(url_for('client.client'))

    except IntegrityError:
        db.session.rollback()
        flash('Não foi possível deletar o cliente.', 'danger')

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
        try:
            data = db.session.get(Client, id)

            if not data:
                flash('cliente não foi encontrado!', 'danger')
                return redirect(url_for('client.client'))

            client_name = request.form.get('name', '').strip()
            client_cpf_cnpj = request.form.get('CPF_CNPJ', '').strip()
            client_email = request.form.get('email', '').strip()
            client_phone = request.form.get('phone', '').strip()

            if not client_name:
                flash('Não foi possível atualizar o cliente, falta o campo nome.', 'danger')
                return redirect(url_for('client.client_update', id=id))

            if not client_cpf_cnpj:
                flash('Não foi possível atualizar o cliente, falta o campo cpf_cnpj.', 'danger')
                return redirect(url_for('client.client_update', id=id))

            if not client_phone:
                flash('Não foi possível atualizar o cliente, falta o campo telefone.', 'danger')
                return redirect(url_for('client.client_update', id=id))

            data.name = client_name
            data.CPF_CNPJ = client_cpf_cnpj
            data.email = client_email
            data.phone = client_phone

            db.session.commit()
            flash('Cliente atualizado com sucesso!', 'success')
            return redirect(url_for('client.client'))
        except IntegrityError:
            db.session.rollback()
            flash('Erro ao atualizar o cliente!', 'danger')
            return redirect(url_for('client.client_update', id=id))
