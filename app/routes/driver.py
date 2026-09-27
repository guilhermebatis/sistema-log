from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.driver import Driver
from app.models.driver import DriverStatus, DrivingLicenceCategory
from datetime import date, datetime


driver_bp = Blueprint('driver', __name__, url_prefix='/driver')

@driver_bp.route('/')
def index():
    data = db.session.query(Driver).all()
    return render_template('driver/index.html', data=data)


@driver_bp.route('/create', methods=['GET', 'POST'])
def driver_create():
    if request.method == 'POST':
        # recive data from form
        driver_name = request.form.get('name', '').strip()
        driver_cnh = request.form.get('cnh', '').strip()
        driver_phone = request.form.get('phone', '').strip()
        driver_admission_date = request.form.get('admission_date', '').strip()
        driver_licence_category = request.form.get('licence_category', '').strip()
        driver_license_expiration_date = request.form.get('license_expiration_date', '').strip()
        driver_status = request.form.get('status', '').strip()

        # data validation
        if not driver_name:
            flash('Não foi possivel criar o motorista, falta a campo nome', 'danger')
            return redirect(url_for('driver.driver_create'))
        if not driver_cnh:
            flash('Não foi possivel criar o motorista, falta a campo cnh', 'danger')
            return redirect(url_for('driver.driver_create'))
        if not driver_phone:
            flash('Não foi possivel criar o motorista, falta a campo telefone', 'danger')
            return redirect(url_for('driver.driver_create'))
        if not driver_admission_date:
            flash('Não foi possivel criar o motorista, falta a campo data de adimissão', 'danger')
            return redirect(url_for('driver.driver_create'))
        if not driver_licence_category:
            flash('Não foi possivel criar o motorista, falta a campo categoria da cnh', 'danger')
            return redirect(url_for('driver.driver_create'))
        if not driver_license_expiration_date:
            flash('Não foi possivel criar o motorista, falta a campo vencinto da cnh', 'danger')
            return redirect(url_for('driver.driver_create'))
        if not driver_status:
            flash('Não foi possivel criar o motorista, falta a campo status', 'danger')
            return redirect(url_for('driver.driver_create'))

        # data tranformation
        try:
            driver_licence_category = DrivingLicenceCategory(driver_licence_category)
            driver_status = DriverStatus(driver_status)
            driver_admission_date = datetime.strptime(driver_admission_date, "%Y-%m-%d").date()
            driver_license_expiration_date = datetime.strptime(driver_license_expiration_date, "%Y-%m-%d").date()

        except ValueError:
            flash('Não foi possivel criar o motorista', 'danger')
            return redirect(url_for('driver.create'))

        #Create drive in database
        new_driver = Driver(
            name = driver_name,
            cnh = driver_cnh,
            phone = driver_phone,
            admission_date = driver_admission_date,
            licence_category = driver_licence_category,
            license_expiration_date = driver_license_expiration_date,
            status = driver_status,
        )

        try:
            db.session.add(new_driver)
            db.session.commit()
            flash('Motorista cadastrado com sucesso', 'success')
            return redirect(url_for('driver.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Erro ao cadastrar o motorista', 'danger')
            return redirect(url_for('driver.index'))

    return render_template("driver/create.html")


@driver_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def driver_update(id):
    if request.method == 'GET':

        data = db.session.get(Driver, id)

        if not data:
            flash('Não foi possivel editar o motorista', 'danger')
            return redirect(url_for('driver.index'))

        return render_template("driver/update.html", data=data)

    if request.method == 'POST':

        data = db.session.get(Driver, id)

        if not data:
            flash('Não foi possivel editar o motorista', 'danger')
            return redirect(url_for('driver.index'))

        driver_name = request.form.get('name', '').strip()
        driver_cnh =  request.form.get('cnh', '').strip()
        driver_phone = request.form.get('phone', '').strip()
        driver_admission_date = request.form.get('admission_date', '').strip()
        driver_licence_category = request.form.get('licence_category', '').strip()
        driver_license_expiration_date = request.form.get('license_expiration_date', '').strip()
        driver_status = request.form.get('status', '').strip()

        # data validation
        if not driver_name:
            flash('Não foi possivel criar o motorista, falta a campo nome', 'danger')
            return redirect(url_for('driver.driver_update', id=id))
        if not driver_cnh:
            flash('Não foi possivel criar o motorista, falta a campo cnh', 'danger')
            return redirect(url_for('driver.driver_update', id=id))
        if not driver_phone:
            flash('Não foi possivel criar o motorista, falta a campo telefone', 'danger')
            return redirect(url_for('driver.driver_update', id=id))
        if not driver_admission_date:
            flash('Não foi possivel criar o motorista, falta a campo data de adimissão', 'danger')
            return redirect(url_for('driver.driver_update', id=id))
        if not driver_licence_category:
            flash('Não foi possivel criar o motorista, falta a campo categoria da cnh', 'danger')
            return redirect(url_for('driver.driver_update', id=id))
        if not driver_license_expiration_date:
            flash('Não foi possivel criar o motorista, falta a campo vencinto da cnh', 'danger')
            return redirect(url_for('driver.driver_update', id=id))
        if not driver_status:
            flash('Não foi possivel criar o motorista, falta a campo status', 'danger')
            return redirect(url_for('driver.driver_update', id=id))

        # data tranformation
        try:
            driver_licence_category = DrivingLicenceCategory(driver_licence_category)
            driver_status = DriverStatus(driver_status)
            driver_admission_date = datetime.strptime(driver_admission_date, "%Y-%m-%d").date()
            driver_license_expiration_date = datetime.strptime(driver_license_expiration_date, "%Y-%m-%d").date()
        except:
            flash('Não foi possivel criar o motorista', 'danger')
            return redirect(url_for('driver.driver_update', id=id))

        try:
            #Update Driver
            data.name = driver_name
            data.cnh = driver_cnh
            data.phone = driver_phone
            data.admission_date = driver_admission_date
            data.licence_category = driver_licence_category
            data.license_expiration_date = driver_license_expiration_date
            data.status = driver_status

            db.session.commit()
            flash('Motorista atualizado com sucesso!', 'success')
            return redirect(url_for('driver.index'))
        except:
            flash('Não foi possivel atualizar o motorista', 'danger')
            return redirect(url_for('driver.driver_update', id=id))


@driver_bp.route('/<int:id>/delete', methods=['POST'])
def driver_delete(id):
    try:

        data = db.session.get(Driver, id)

        if not data:
            flash('Não foi possivel editar o motorista', 'danger')
            return redirect(url_for('driver.index'))

        db.session.delete(data)
        db.session.commit()
        flash('Motorista deletado com sucesso!', 'success')
        return redirect(url_for('driver.index'))

    except IntegrityError:
        db.session.rollback()
        flash('Não foi possivel deletar o motorista', 'danger')
        return redirect(url_for('driver.index'))