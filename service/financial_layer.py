from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.financial_entry import FinancialEntry
from app.models.financial_installment import FinancialInstallment, StatusFinancialInstallment
from app.models.financial_payment import FinancialPayment
from flask import flash
from decimal import Decimal


def _validate_financial_entry_create(financial_entry: FinancialEntry):
    if financial_entry.type is None:
        flash('O tipo de operação e obrigatorio', 'danger')
        return False
    if financial_entry.created_by is None:
        flash('O usuario que criou e obrigatorio', 'danger')
        return False
    if financial_entry.total_amount is None:
        flash('O valor total e obrigatorio', 'danger')
        return False
    if financial_entry.total_amount <= 0:
        flash('O valor total não pode ser 0 ou negativo', 'danger')
        return False
    if financial_entry.description is None:
        flash('A descrição e obrigatorio', 'danger')
        return False
    return True


def _validate_financial_entry_update(financial_entry: FinancialEntry):
    if financial_entry.id is not None:
        if financial_entry.type is None:
            flash('O tipo de operação e obrigatorio', 'danger')
            return False
        if financial_entry.total_amount is None:
            flash('O valor total e obrigatorio', 'danger')
            return False
        if financial_entry.total_amount <= 0:
            flash('O valor total não pode ser 0 ou negativo', 'danger')
            return False
        if financial_entry.description is None:
            flash('A descrição e obrigatorio', 'danger')
            return False
    else:
        flash('É necessário informar o ID para atualizar', 'danger')
        return False
    return True


def _validate_financial_installment(financial_installments: list[FinancialInstallment]):

    if len(financial_installments) == 0:
        return False

    for financial_installment in financial_installments:
        if financial_installment.amount is None:
            flash('O valor da parcela e obrigatorio', 'danger')
            return False
        if financial_installment.amount <= 0:
            flash('O valor da parcela nao pode ser 0 ou negativo', 'danger')
            return False
        if financial_installment.due_date is None:
            flash('A data de vencimento e obrigatorio', 'danger')
            return False

    return True


def _validate_installments_total_create(financial_entry,
                                 financial_installments: list[FinancialInstallment]):

    total_amount = Decimal("0.00")

    for financial_installment in financial_installments:
        total_amount += financial_installment.amount

    if total_amount != financial_entry.total_amount:
        flash('O valor total das parcelas e diferente do que o valor total da entrada', 'danger')
        return False

    return True


def _validate_installments_total_update(
    financial_entry_data: FinancialEntry,
    financial_installments: list[FinancialInstallment],
    new_total_amount: Decimal
):

    financial_installments_data = financial_entry_data.financial_installments
    total_amount = Decimal("0.00")


    for financial_installment in financial_installments:

        if financial_installment.id is None:
            total_amount += financial_installment.amount
        else:

            for financial_installment_data in financial_installments_data:

                found = False
                if financial_installment_data.id == financial_installment.id:
                    if financial_installment_data.status == StatusFinancialInstallment.PAID:
                        total_amount += financial_installment_data.amount
                        found = True
                        break

                    total_amount += financial_installment.amount
                    found = True
                    break
            if not found:
                flash('Não foi possivel localizar a parcela para atualizar', 'danger')
                return False

    id_total_update = []
    for financial_installment in financial_installments:
        if financial_installment.id is not None:
            id_total_update.append(financial_installment.id)

    if len(id_total_update) != len(set(id_total_update)):
        flash('Existem parcelas duplicadas na atualização', 'danger')
        return False

    id_total_data = []
    for financial_installment_data in financial_installments_data:
        if financial_installment_data.status == StatusFinancialInstallment.PAID:
            id_total_data.append(financial_installment_data.id)

    if not set(id_total_data).issubset(set(id_total_update)):
        flash('Não é permitido remover parcelas já pagas', 'danger')
        return False

    if total_amount != new_total_amount:
        flash('O valor total das parcelas é diferente do valor total da entrada', 'danger')
        return False

    return True


def create_financial_entry(financial_entry: FinancialEntry,
                           financial_installments: list[FinancialInstallment]):

    if not _validate_financial_entry_create(financial_entry):
        return False
    if not _validate_financial_installment(financial_installments):
        return False
    if not _validate_installments_total_create(financial_entry, financial_installments):
        return False

    try:
        for financial_installment in financial_installments:
            financial_installment.status = StatusFinancialInstallment.PENDING
            financial_installment.financial_entry = financial_entry

        db.session.add(financial_entry)

        for financial_installment in financial_installments:
            # pyrefly: ignore[bad-assignment]
            financial_installment.financial_entry = financial_entry

        db.session.add_all(financial_installments)
        db.session.commit()
        flash('Entrada financeira foi criada com sucesso', 'success')
        return True

    except IntegrityError:
        db.session.rollback()
        flash('Error ao criar a entrada financeira', 'danger')
        return False


def update_financial_entry(financial_entry: FinancialEntry,
                           financial_installments: list[FinancialInstallment]):

    financial_entry_data = db.session.get(FinancialEntry, financial_entry.id)

    if not financial_entry_data:
        return False

    financial_installments_data = financial_entry_data.financial_installments

    if not _validate_financial_entry_update(financial_entry):
        return False

    if not _validate_financial_installment(financial_installments):
        return False

    if not _validate_installments_total_update(financial_entry_data,
                                               financial_installments,
                                               financial_entry.total_amount
    ):
        return False

    try:
        incoming_ids = [
            financial_installment.id
            for financial_installment in financial_installments
            if financial_installment.id is not None
        ]

        for financial_installment_data in financial_installments_data:

            # Parcelas pagas permanecem intactas.
            if financial_installment_data.status == StatusFinancialInstallment.PAID:
                continue

            # Remove parcelas pendentes que não foram recebidas.
            if financial_installment_data.id not in incoming_ids:
                db.session.delete(financial_installment_data)
                continue

            # Atualiza parcelas pendentes existentes.
            for financial_installment in financial_installments:
                if financial_installment.id == financial_installment_data.id:
                    financial_installment_data.amount = financial_installment.amount
                    financial_installment_data.due_date = financial_installment.due_date
                    break

        # Adiciona novas parcelas.
        for financial_installment in financial_installments:
            if financial_installment.id is None:
                financial_installment.financial_entry = financial_entry_data
                db.session.add(financial_installment)

        # Atualiza os dados da entrada.
        financial_entry_data.type = financial_entry.type
        financial_entry_data.total_amount = financial_entry.total_amount
        financial_entry_data.description = financial_entry.description

        db.session.commit()

        flash('Entrada financeira atualizada com sucesso!', 'success')
        return True

    except IntegrityError:
        db.session.rollback()
        flash('Error ao atualizar a entrada financeira', 'danger')
        return False


def _validate_financial_payment(financial_payment: FinancialPayment):
    if financial_payment.financial_installment is None:
        flash('Não exitem pacelas pendentes', 'danger')
        return False
    if financial_payment.financial_installment.status == StatusFinancialInstallment.PAID:
        flash('Pagamento ja realizado', 'danger')
        return False

    if financial_payment.payment_date is None:
        flash('O campo data do pagamento e obrigatorio', 'danger')
        return False
    if financial_payment.created_by is None:
        flash('O campo criado por e obrigatorio', 'danger')
        return False
    return True


def create_financial_payment(financial_payment: FinancialPayment):
    if not _validate_financial_payment(financial_payment):
        return False

    try:
        db.session.add(financial_payment)
        financial_payment.financial_installment.status = StatusFinancialInstallment.PAID
        db.session.commit()
        flash('Pagamento foi realizado com sucesso', 'success')
        return True
    except IntegrityError:
        db.session.rollback()
        flash('Error ao criar o pagamento', 'danger')
        return False