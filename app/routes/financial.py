from decimal import Decimal, InvalidOperation

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.models.financial_installment import FinancialInstallment
from app.models.financial_entry import FinancialEntry, FinancialEntryType
from app.models.financial_payment import FinancialPayment

from service.financial_layer import create_financial_entry, update_financial_entry


financial_bp = Blueprint('financial', __name__, url_prefix='/financial')

@financial_bp.route('/', methods=['GET'])
@login_required
def index():
    financial_entry_data = FinancialEntry.query.all()

    return render_template('financial/index.html',
                           financial_entry_data=financial_entry_data,)


@financial_bp.route('/<int:id>/info', methods=['GET'])
@login_required
def info(id):
    financial_entry_data = FinancialEntry.query.get(id)

    if financial_entry_data is None:
        flash('Financial entry not found.', 'warning')
        return redirect(url_for('financial.index'))

    return render_template(
        'financial/info.html',
        financial_entry_data=financial_entry_data
    )


@financial_bp.route('/create_entry', methods=['GET', 'POST'])
@login_required
def create_entry():
    if request.method == 'GET':
        return render_template('financial/create_entry.html')

    if request.method == 'POST':
        financial_entry_type = request.form.get('financial_entry_type', '').strip()
        financial_entry_total_amount = request.form.get('financial_entry_total_amount', '').strip()
        financial_entry_description = request.form.get('financial_entry_description', '').strip()

        try:
            financial_entry_type = FinancialEntryType(financial_entry_type)
            financial_entry_total_amount = Decimal(financial_entry_total_amount)

            financial_entry = FinancialEntry(
                type=financial_entry_type,
                created_by=current_user.id,
                total_amount=financial_entry_total_amount,
                description=financial_entry_description,
            )

        except (ValueError, InvalidOperation):
            flash('Please enter a valid financial entry type.')
            return render_template('financial/create_entry.html',)

        financial_installment_amount = request.form.get('financial_installment_amount', '').strip()
        financial_installment_due_date = request.form.get('financial_installment_due_date', '').strip()

        try:
            financial_installment_amount = Decimal(financial_installment_amount)
            financial_installment_due_date = datetime.strptime(financial_installment_due_date, "%Y-%m-%d").date()

            financial_installment = FinancialInstallment(
                amount=financial_installment_amount,
                due_date=financial_installment_due_date,
            )

        except (ValueError, InvalidOperation):
            flash('Please enter a valid financial entry type.')
            return render_template('financial/create_entry.html', )

        if create_financial_entry(financial_entry, [financial_installment]):
            return redirect(url_for('financial.index'))
        else:
            flash('Please enter a valid financial entry type.')
            return render_template('financial/create_entry.html', )


@financial_bp.route('/<int:id>/update_entry', methods=['GET', 'POST'])
@login_required
def update_entry(id):
    if request.method == 'GET':
        financial_entry_data = FinancialEntry.query.get(id)

        if financial_entry_data is None:
            flash('Please enter a valid financial entry type.')
            return redirect(url_for('financial.index'))

        financial_installment_data = financial_entry_data.financial_installments
        return render_template('financial/update_entry.html',
                               financial_entry_data=financial_entry_data,
                               financial_installment_data=financial_installment_data)

    if request.method == 'POST':

        financial_entry_data = FinancialEntry.query.get(id)

        if financial_entry_data is None:
            flash('Please enter a valid financial entry type.')
            return redirect(url_for('financial.index'))


        financial_entry_type = request.form.get('financial_entry_type', '').strip()
        financial_entry_total_amount = request.form.get('financial_entry_total_amount', '').strip()
        financial_entry_description = request.form.get('financial_entry_description', '').strip()

        try:
            financial_entry_type = FinancialEntryType(financial_entry_type)
            financial_entry_total_amount = Decimal(financial_entry_total_amount)
            financial_entry_description = str(financial_entry_description)

            financial_entry = FinancialEntry(
                id=financial_entry_data.id,
                type=financial_entry_type,
                total_amount=financial_entry_total_amount,
                description=financial_entry_description,
            )

        except (ValueError, InvalidOperation):
            flash('Please enter a valid financial entry type.')
            return redirect(url_for('financial.update_entry', id=id))

        financial_installment_amount = request.form.get('financial_installment_amount', '').strip()
        financial_installment_due_date = request.form.get('financial_installment_due_date', '').strip()

        try:
            financial_installment_amount = Decimal(financial_installment_amount)
            financial_installment_due_date = datetime.strptime(financial_installment_due_date, "%Y-%m-%d").date()

            financial_installment = FinancialInstallment(
                amount=financial_installment_amount,
                due_date=financial_installment_due_date,
            )

        except (ValueError, InvalidOperation):
            flash('Please enter a valid financial entry type.')
            return redirect(url_for('financial.update_entry', id=id))


        if update_financial_entry(financial_entry, [financial_installment]):
            flash('Financial entry successfully updated.')
            return redirect(url_for('financial.index'))
        else:
            flash('Please enter a valid financial entry type.')
            return redirect(url_for('financial.update_entry', id=id))