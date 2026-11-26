import datetime
from decimal import Decimal

import pytest

from app.extensions import db
from app.models import FinancialPayment
from app.models.user import User
from app.models.financial_entry import FinancialEntry, FinancialEntryType
from app.models.financial_installment import (
    FinancialInstallment,
    StatusFinancialInstallment,
)

from service.financial_layer import (
    create_financial_entry,
    update_financial_entry,
    create_financial_payment,
)


def create_test_user():
    user = User(
        username="test1",
        name="name_test",
        email="test_email_test",
        password_hash="123456",
        is_active=True,
        role="user",
    )

    db.session.add(user)
    db.session.flush()

    return user


def create_entry_with_installments(user, amounts):
    """Cria uma entrada de teste e retorna a entrada e suas parcelas."""
    financial_entry = FinancialEntry(
        type=FinancialEntryType.PAYABLE,
        created_by=user.id,
        total_amount=sum(amounts, Decimal("0.00")),
        description="Teste financeiro",
    )

    financial_installments = [
        FinancialInstallment(
            amount=amount,
            due_date=datetime.date.today(),
        )
        for amount in amounts
    ]

    result = create_financial_entry(
        financial_entry,
        financial_installments,
    )

    assert result is True

    return financial_entry, financial_installments


# ---------------------------------------------------------------------
# CREATE FINANCIAL ENTRY
# ---------------------------------------------------------------------

def test_financial_entry_one_installment(app):
    with app.test_request_context():
        user = create_test_user()

        financial_entry = FinancialEntry(
            type=FinancialEntryType.PAYABLE,
            created_by=user.id,
            total_amount=Decimal("1000.00"),
            description="cost",
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
            financial_installments,
        )

        financial_entry_data = db.session.get(
            FinancialEntry,
            financial_entry.id,
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
        assert (
                financial_installments_data[0].status
                == StatusFinancialInstallment.PENDING
        )


def test_financial_entry_three_installments(app):
    with app.test_request_context():
        user = create_test_user()

        financial_entry = FinancialEntry(
            type=FinancialEntryType.PAYABLE,
            created_by=user.id,
            total_amount=Decimal("1000.00"),
            description="cost",
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
            ),
        ]

        result = create_financial_entry(
            financial_entry,
            financial_installments,
        )

        financial_entry_data = db.session.get(
            FinancialEntry,
            financial_entry.id,
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


def test_financial_entry_without_installments(app):
    with app.test_request_context():
        user = create_test_user()

        financial_entry = FinancialEntry(
            type=FinancialEntryType.PAYABLE,
            created_by=user.id,
            total_amount=Decimal("1000.00"),
            description="cost",
        )

        result = create_financial_entry(financial_entry, [])

        assert result is False
        assert db.session.query(FinancialEntry).count() == 0
        assert db.session.query(FinancialInstallment).count() == 0


def test_financial_entry_installments_total_mismatch(app):
    with app.test_request_context():
        user = create_test_user()

        financial_entry = FinancialEntry(
            type=FinancialEntryType.PAYABLE,
            created_by=user.id,
            total_amount=Decimal("1000.00"),
            description="cost",
        )

        financial_installments = [
            FinancialInstallment(
                amount=Decimal("300.00"),
                due_date=datetime.date.today(),
            ),
            FinancialInstallment(
                amount=Decimal("500.00"),
                due_date=datetime.date.today(),
            ),
        ]

        result = create_financial_entry(
            financial_entry,
            financial_installments,
        )

        assert result is False
        assert db.session.query(FinancialEntry).count() == 0
        assert db.session.query(FinancialInstallment).count() == 0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("type", None),
        ("created_by", None),
        ("total_amount", None),
        ("total_amount", Decimal("0.00")),
        ("total_amount", Decimal("-100.00")),
        ("description", None),
    ],
)
def test_financial_entry_invalid_fields(app, field, value):
    with app.test_request_context():
        user = create_test_user()

        financial_entry = FinancialEntry(
            type=FinancialEntryType.PAYABLE,
            created_by=user.id,
            total_amount=Decimal("100.00"),
            description="Teste",
        )
        setattr(financial_entry, field, value)

        installments = [
            FinancialInstallment(
                amount=Decimal("100.00"),
                due_date=datetime.date.today(),
            )
        ]

        result = create_financial_entry(financial_entry, installments)

        assert result is False
        assert db.session.query(FinancialEntry).count() == 0
        assert db.session.query(FinancialInstallment).count() == 0


@pytest.mark.parametrize(
    ("amount", "due_date"),
    [
        (None, datetime.date.today()),
        (Decimal("0.00"), datetime.date.today()),
        (Decimal("-10.00"), datetime.date.today()),
        (Decimal("100.00"), None),
    ],
)
def test_financial_installment_invalid_fields(app, amount, due_date):
    with app.test_request_context():
        user = create_test_user()

        financial_entry = FinancialEntry(
            type=FinancialEntryType.PAYABLE,
            created_by=user.id,
            total_amount=Decimal("100.00"),
            description="Teste",
        )

        installments = [
            FinancialInstallment(
                amount=amount,
                due_date=due_date,
            )
        ]

        result = create_financial_entry(financial_entry, installments)

        assert result is False
        assert db.session.query(FinancialEntry).count() == 0
        assert db.session.query(FinancialInstallment).count() == 0



def test_financial_entry_new_installment_must_be_pending(app):
    """Regra esperada: novas parcelas sempre começam como PENDING."""
    with app.test_request_context():
        user = create_test_user()

        financial_entry = FinancialEntry(
            type=FinancialEntryType.PAYABLE,
            created_by=user.id,
            total_amount=Decimal("100.00"),
            description="Teste",
        )

        installments = [
            FinancialInstallment(
                amount=Decimal("100.00"),
                status=StatusFinancialInstallment.PAID,
                due_date=datetime.date.today(),
            )
        ]

        result = create_financial_entry(financial_entry, installments)

        assert result is True
        assert installments[0].status == StatusFinancialInstallment.PENDING


# ---------------------------------------------------------------------
# UPDATE FINANCIAL ENTRY
# ---------------------------------------------------------------------

def test_update_financial_entry_installments(app):
    with app.test_request_context():
        user = create_test_user()

        financial_entry, installments = create_entry_with_installments(
            user,
            [Decimal("300.00"), Decimal("700.00")],
        )

        updated_entry = FinancialEntry(
            id=financial_entry.id,
            type=FinancialEntryType.RECEIVABLE,
            total_amount=Decimal("1000.00"),
            description="Entrada atualizada",
        )

        updated_installments = [
            FinancialInstallment(
                id=installments[0].id,
                amount=Decimal("400.00"),
                due_date=datetime.date.today(),
            ),
            FinancialInstallment(
                amount=Decimal("600.00"),
                due_date=datetime.date.today(),
            ),
        ]

        result = update_financial_entry(
            updated_entry,
            updated_installments,
        )

        db.session.expire_all()

        entry_data = db.session.get(FinancialEntry, financial_entry.id)

        installments_data = (
            db.session.query(FinancialInstallment)
            .filter_by(financial_entry_id=financial_entry.id)
            .all()
        )

        assert result is True
        assert entry_data.description == "Entrada atualizada"
        assert entry_data.type == FinancialEntryType.RECEIVABLE
        assert len(installments_data) == 2

        amounts = sorted(item.amount for item in installments_data)
        assert amounts == [Decimal("400.00"), Decimal("600.00")]


def test_update_financial_entry_preserves_paid_installment(app):
    with app.test_request_context():
        user = create_test_user()

        financial_entry, installments = create_entry_with_installments(
            user,
            [Decimal("300.00"), Decimal("700.00")],
        )

        paid_installment = db.session.get(
            FinancialInstallment,
            installments[0].id,
        )

        payment = FinancialPayment(
            financial_installment=paid_installment,
            payment_date=datetime.date.today(),
            created_by=user.id,
        )
        assert create_financial_payment(payment) is True

        updated_entry = FinancialEntry(
            id=financial_entry.id,
            type=FinancialEntryType.PAYABLE,
            total_amount=Decimal("1000.00"),
            description="Atualização",
        )

        updated_installments = [
            FinancialInstallment(
                id=installments[0].id,
                amount=Decimal("999.00"),
                due_date=datetime.date.today(),
            ),
            FinancialInstallment(
                id=installments[1].id,
                amount=Decimal("700.00"),
                due_date=datetime.date.today(),
            ),
        ]

        result = update_financial_entry(
            updated_entry,
            updated_installments,
        )

        db.session.expire_all()

        paid_installment_data = db.session.get(
            FinancialInstallment,
            installments[0].id,
        )

        assert result is True
        assert paid_installment_data.amount == Decimal("300.00")
        assert paid_installment_data.status == StatusFinancialInstallment.PAID


def test_update_financial_entry_cannot_remove_paid_installment(app):
    with app.test_request_context():
        user = create_test_user()

        financial_entry, installments = create_entry_with_installments(
            user,
            [Decimal("300.00"), Decimal("700.00")],
        )

        paid_installment = db.session.get(
            FinancialInstallment,
            installments[0].id,
        )

        payment = FinancialPayment(
            financial_installment=paid_installment,
            payment_date=datetime.date.today(),
            created_by=user.id,
        )
        assert create_financial_payment(payment) is True

        updated_entry = FinancialEntry(
            id=financial_entry.id,
            type=FinancialEntryType.PAYABLE,
            total_amount=Decimal("700.00"),
            description="Atualização",
        )

        updated_installments = [
            FinancialInstallment(
                id=installments[1].id,
                amount=Decimal("700.00"),
                due_date=datetime.date.today(),
            )
        ]

        result = update_financial_entry(
            updated_entry,
            updated_installments,
        )

        assert result is False

        paid_installment_data = db.session.get(
            FinancialInstallment,
            installments[0].id,
        )

        assert paid_installment_data is not None
        assert paid_installment_data.status == StatusFinancialInstallment.PAID


def test_update_financial_entry_rejects_foreign_installment_id(app):
    with app.test_request_context():
        user = create_test_user()

        entry_one, _ = create_entry_with_installments(
            user,
            [Decimal("500.00")],
        )
        entry_two, installments_two = create_entry_with_installments(
            user,
            [Decimal("500.00")],
        )

        updated_entry = FinancialEntry(
            id=entry_one.id,
            type=FinancialEntryType.PAYABLE,
            total_amount=Decimal("500.00"),
            description="Tentativa de alteração",
        )

        incoming_installments = [
            FinancialInstallment(
                id=installments_two[0].id,
                amount=Decimal("500.00"),
                due_date=datetime.date.today(),
            )
        ]

        result = update_financial_entry(
            updated_entry,
            incoming_installments,
        )

        assert result is False

        db.session.expire_all()
        foreign_installment = db.session.get(
            FinancialInstallment,
            installments_two[0].id,
        )

        assert foreign_installment.financial_entry_id == entry_two.id


def test_update_financial_entry_rejects_duplicate_installment_ids(app):
    with app.test_request_context():
        user = create_test_user()

        financial_entry, installments = create_entry_with_installments(
            user,
            [Decimal("500.00")],
        )

        updated_entry = FinancialEntry(
            id=financial_entry.id,
            type=FinancialEntryType.PAYABLE,
            total_amount=Decimal("1000.00"),
            description="Atualização",
        )

        incoming_installments = [
            FinancialInstallment(
                id=installments[0].id,
                amount=Decimal("500.00"),
                due_date=datetime.date.today(),
            ),
            FinancialInstallment(
                id=installments[0].id,
                amount=Decimal("500.00"),
                due_date=datetime.date.today(),
            ),
        ]

        result = update_financial_entry(
            updated_entry,
            incoming_installments,
        )

        assert result is False


def test_update_financial_entry_not_found(app):
    with app.test_request_context():
        updated_entry = FinancialEntry(
            id=999999,
            type=FinancialEntryType.PAYABLE,
            total_amount=Decimal("100.00"),
            description="Teste",
        )

        installments = [
            FinancialInstallment(
                amount=Decimal("100.00"),
                due_date=datetime.date.today(),
            )
        ]

        result = update_financial_entry(updated_entry, installments)

        assert result is False


# ---------------------------------------------------------------------
# CREATE FINANCIAL PAYMENT
# ---------------------------------------------------------------------

def test_financial_payment_one_installment(app):
    with app.test_request_context():
        user = create_test_user()

        financial_entry, installments = create_entry_with_installments(
            user,
            [
                Decimal("100.00"),
                Decimal("500.00"),
                Decimal("400.00"),
            ],
        )

        financial_installment = db.session.get(
            FinancialInstallment,
            installments[0].id,
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
                financial_installment_id=financial_installment.id,
            )
            .first()
        )

        db.session.expire_all()
        financial_installment_data = db.session.get(
            FinancialInstallment,
            financial_installment.id,
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


def test_financial_payment_already_paid(app):
    with app.test_request_context():
        user = create_test_user()

        _, installments = create_entry_with_installments(
            user,
            [Decimal("1000.00")],
        )

        financial_installment = db.session.get(
            FinancialInstallment,
            installments[0].id,
        )

        first_payment = FinancialPayment(
            financial_installment=financial_installment,
            payment_date=datetime.date.today(),
            created_by=user.id,
        )
        first_result = create_financial_payment(first_payment)

        # Usa a chave estrangeira diretamente para não substituir
        # o relacionamento one-to-one que já existe em memória.
        second_payment = FinancialPayment(
            financial_installment_id=financial_installment.id,
            payment_date=datetime.date.today(),
            created_by=user.id,
        )
        second_result = create_financial_payment(second_payment)

        payments = (
            db.session.query(FinancialPayment)
            .filter_by(
                financial_installment_id=financial_installment.id,
            )
            .all()
        )

        assert first_result is True
        assert second_result is False
        assert len(payments) == 1
        assert financial_installment.status == StatusFinancialInstallment.PAID


@pytest.mark.parametrize(
    ("payment_date", "created_by"),
    [
        (None, 1),
        (datetime.date.today(), None),
    ],
)
def test_financial_payment_invalid_required_fields(
        app,
        payment_date,
        created_by,
):
    with app.test_request_context():
        user = create_test_user()

        _, installments = create_entry_with_installments(
            user,
            [Decimal("100.00")],
        )

        financial_installment = db.session.get(
            FinancialInstallment,
            installments[0].id,
        )

        payment = FinancialPayment(
            financial_installment=financial_installment,
            payment_date=payment_date,
            created_by=created_by,
        )

        result = create_financial_payment(payment)

        assert result is False
        assert db.session.query(FinancialPayment).count() == 0
        assert (
                financial_installment.status
                == StatusFinancialInstallment.PENDING
        )


def test_financial_payment_without_installment(app):
    with app.test_request_context():
        user = create_test_user()

        payment = FinancialPayment(
            payment_date=datetime.date.today(),
            created_by=user.id,
        )

        result = create_financial_payment(payment)

        assert result is False
        assert db.session.query(FinancialPayment).count() == 0
