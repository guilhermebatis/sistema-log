
import datetime
from decimal import Decimal

from app.extensions import db
from app.models import FinancialPayment
from app.models.user import User
from app.models.financial_entry import FinancialEntry, FinancialEntryType
from app.models.financial_installment import (
    FinancialInstallment,
    StatusFinancialInstallment
)

from service.financial_layer import (
    create_financial_entry,
    create_financial_payment
)


def create_test_user():
    user = User(
        username='test1',
        name='name_test',
        email='test_email_test',
        password_hash='123456',
        is_active=True,
        role='user',
    )

    db.session.add(user)
    db.session.flush()

    return user


def test_financial_entry_one_installment(app):
    with app.test_request_context():

        user = create_test_user()

        financial_entry = FinancialEntry(
            type=FinancialEntryType.PAYABLE,
            created_by=user.id,
            total_amount=Decimal("1000.00"),
            description='cost',
        )

        financial_installments = [
            FinancialInstallment(
                amount=Decimal("1000.00"),
                status=StatusFinancialInstallment.PENDING,
                due_date=datetime.date.today(),
            )
        ]

        result = create_financial_entry(
            financial_entry,
            financial_installments
        )

        financial_entry_data = db.session.get(
            FinancialEntry,
            financial_entry.id
        )

        financial_installments_data = (
            db.session.query(FinancialInstallment)
            .filter_by(financial_entry_id=financial_entry.id)
            .all()
        )

        assert result is True
        assert financial_entry_data is not None
        assert len(financial_installments_data) == 1
        assert financial_installments_data[0].amount == Decimal("1000.00")
        assert financial_installments_data[0].status == StatusFinancialInstallment.PENDING


def test_financial_entry_three_installments(app):
    with app.test_request_context():

        user = create_test_user()

        financial_entry = FinancialEntry(
            type=FinancialEntryType.PAYABLE,
            created_by=user.id,
            total_amount=Decimal("1000.00"),
            description='cost',
        )

        financial_installments = [
            FinancialInstallment(
                amount=Decimal("100.00"),
                status=StatusFinancialInstallment.PENDING,
                due_date=datetime.date.today(),
            ),
            FinancialInstallment(
                amount=Decimal("500.00"),
                status=StatusFinancialInstallment.PENDING,
                due_date=datetime.date.today(),
            ),
            FinancialInstallment(
                amount=Decimal("400.00"),
                status=StatusFinancialInstallment.PENDING,
                due_date=datetime.date.today(),
            )
        ]

        result = create_financial_entry(
            financial_entry,
            financial_installments
        )

        financial_entry_data = db.session.get(
            FinancialEntry,
            financial_entry.id
        )

        financial_installments_data = (
            db.session.query(FinancialInstallment)
            .filter_by(financial_entry_id=financial_entry.id)
            .all()
        )

        total_installments = sum(
            installment.amount
            for installment in financial_installments_data
        )

        assert result is True
        assert financial_entry_data is not None
        assert len(financial_installments_data) == 3
        assert total_installments == Decimal("1000.00")

        for installment in financial_installments_data:
            assert installment.status == StatusFinancialInstallment.PENDING


def test_financial_payment_one_installment(app):
    with app.test_request_context():

        user = create_test_user()

        financial_entry = FinancialEntry(
            type=FinancialEntryType.PAYABLE,
            created_by=user.id,
            total_amount=Decimal("1000.00"),
            description='cost',
        )

        financial_installments = [
            FinancialInstallment(
                amount=Decimal("100.00"),
                status=StatusFinancialInstallment.PENDING,
                due_date=datetime.date.today(),
            ),
            FinancialInstallment(
                amount=Decimal("500.00"),
                status=StatusFinancialInstallment.PENDING,
                due_date=datetime.date.today(),
            ),
            FinancialInstallment(
                amount=Decimal("400.00"),
                status=StatusFinancialInstallment.PENDING,
                due_date=datetime.date.today(),
            )
        ]

        entry_result = create_financial_entry(
            financial_entry,
            financial_installments
        )

        assert entry_result is True

        financial_installment = db.session.get(
            FinancialInstallment,
            financial_installments[0].id
        )

        assert financial_installment is not None

        financial_payment = FinancialPayment(
            financial_installment=financial_installment,
            payment_date=datetime.date.today(),
            created_by=user.id,
        )

        payment_result = create_financial_payment(financial_payment)

        financial_payment_data = (
            db.session.query(FinancialPayment)
            .filter_by(
                financial_installment_id=financial_installment.id
            )
            .first()
        )

        financial_installment_data = db.session.get(
            FinancialInstallment,
            financial_installment.id
        )

        financial_installments_data = (
            db.session.query(FinancialInstallment)
            .filter_by(financial_entry_id=financial_entry.id)
            .all()
        )

        assert payment_result is True
        assert financial_payment_data is not None
        assert len(financial_installments_data) == 3
        assert financial_installment_data.status == StatusFinancialInstallment.PAID
        assert financial_payment_data.created_by == user.id
        assert financial_payment_data.payment_date == datetime.date.today()


def test_financial_entry_without_installments(app):
    with app.test_request_context():

        user = create_test_user()

        financial_entry = FinancialEntry(
            type=FinancialEntryType.PAYABLE,
            created_by=user.id,
            total_amount=Decimal("1000.00"),
            description='cost',
        )

        result = create_financial_entry(
            financial_entry,
            []
        )

        financial_entry_data = (
            db.session.query(FinancialEntry).all()
        )

        assert result is False
        assert len(financial_entry_data) == 0


def test_financial_entry_installments_total_mismatch(app):
    with app.test_request_context():

        user = create_test_user()

        financial_entry = FinancialEntry(
            type=FinancialEntryType.PAYABLE,
            created_by=user.id,
            total_amount=Decimal("1000.00"),
            description='cost',
        )

        financial_installments = [
            FinancialInstallment(
                amount=Decimal("300.00"),
                due_date=datetime.date.today(),
            ),
            FinancialInstallment(
                amount=Decimal("500.00"),
                due_date=datetime.date.today(),
            )
        ]

        result = create_financial_entry(
            financial_entry,
            financial_installments
        )

        financial_entry_data = (
            db.session.query(FinancialEntry).all()
        )

        financial_installments_data = (
            db.session.query(FinancialInstallment).all()
        )

        assert result is False
        assert len(financial_entry_data) == 0
        assert len(financial_installments_data) == 0


def test_financial_payment_already_paid(app):
    with app.test_request_context():

        user = create_test_user()

        financial_entry = FinancialEntry(
            type=FinancialEntryType.PAYABLE,
            created_by=user.id,
            total_amount=Decimal("1000.00"),
            description='cost',
        )

        financial_installments = [
            FinancialInstallment(
                amount=Decimal("1000.00"),
                due_date=datetime.date.today(),
            )
        ]

        entry_result = create_financial_entry(
            financial_entry,
            financial_installments
        )

        assert entry_result is True

        financial_installment = db.session.get(
            FinancialInstallment,
            financial_installments[0].id
        )

        financial_payment = FinancialPayment(
            financial_installment=financial_installment,
            payment_date=datetime.date.today(),
            created_by=user.id,
        )

        first_payment_result = create_financial_payment(
            financial_payment
        )

        second_payment = FinancialPayment(
            financial_installment_id=financial_installment.id,
            payment_date=datetime.date.today(),
            created_by=user.id,
        )

        second_payment_result = create_financial_payment(
            second_payment
        )

        payments = (
            db.session.query(FinancialPayment)
            .filter_by(
                financial_installment_id=financial_installment.id
            )
            .all()
        )

        assert first_payment_result is True
        assert second_payment_result is False
        assert len(payments) == 1
        assert financial_installment.status == StatusFinancialInstallment.PAID


def test_financial_payment_duplicate_installment(app):
    with app.test_request_context():

        user = create_test_user()

        financial_entry = FinancialEntry(
            type=FinancialEntryType.PAYABLE,
            created_by=user.id,
            total_amount=Decimal("1000.00"),
            description='cost',
        )

        financial_installments = [
            FinancialInstallment(
                amount=Decimal("1000.00"),
                due_date=datetime.date.today(),
            )
        ]

        entry_result = create_financial_entry(
            financial_entry,
            financial_installments
        )

        assert entry_result is True

        financial_installment = db.session.get(
            FinancialInstallment,
            financial_installments[0].id
        )

        first_payment = FinancialPayment(
            financial_installment=financial_installment,
            payment_date=datetime.date.today(),
            created_by=user.id,
        )

        first_result = create_financial_payment(first_payment)

        second_payment = FinancialPayment(
            financial_installment_id=financial_installment.id,
            payment_date=datetime.date.today(),
            created_by=user.id,
        )

        second_result = create_financial_payment(second_payment)

        payments = (
            db.session.query(FinancialPayment)
            .filter_by(
                financial_installment_id=financial_installment.id
            )
            .all()
        )

        assert first_result is True
        assert second_result is False
        assert len(payments) == 1
