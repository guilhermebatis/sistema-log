import datetime
from decimal import Decimal

import pytest

from app.extensions import db
from app.models.user import User
from app.models.financial_entry import FinancialEntry, FinancialEntryType
from app.models.financial_installment import (
    FinancialInstallment,
    StatusFinancialInstallment,
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
    db.session.commit()

    return user.id


def authenticate_client(client, user_id):
    with client.session_transaction() as session:
        session["_user_id"] = str(user_id)
        session["_fresh"] = True


# ---------------------------------------------------------------------
# CREATE FINANCIAL ENTRY ROUTE
# ---------------------------------------------------------------------

def test_create_financial_entry_get(app, client):
    with app.app_context():
        user = create_test_user()

    authenticate_client(client, user)

    response = client.get("/financial/create_entry")

    assert response.status_code == 200


def test_create_financial_entry_post_success(app, client):
    with app.app_context():
        user = create_test_user()

    authenticate_client(client, user)

    response = client.post(
        "/financial/create_entry",
        data={
            "financial_entry_type": "PAYABLE",
            "financial_entry_total_amount": "1000.00",
            "financial_entry_description": "Teste financeiro",
            "financial_installment_amount": "1000.00",
            "financial_installment_due_date": "2026-12-10",
        },
    )

    assert response.status_code == 302
    assert response.location.endswith("/financial/")

    with app.app_context():
        financial_entry = FinancialEntry.query.first()

        assert financial_entry is not None
        assert financial_entry.type == FinancialEntryType.PAYABLE
        assert financial_entry.created_by == user
        assert financial_entry.total_amount == Decimal("1000.00")
        assert financial_entry.description == "Teste financeiro"

        installments = FinancialInstallment.query.filter_by(
            financial_entry_id=financial_entry.id
        ).all()

        assert len(installments) == 1
        assert installments[0].amount == Decimal("1000.00")
        assert installments[0].due_date == datetime.date(2026, 12, 10)
        assert installments[0].status == StatusFinancialInstallment.PENDING


def test_create_financial_entry_invalid_type(app, client):
    with app.app_context():
        user = create_test_user()

    authenticate_client(client, user)

    response = client.post(
        "/financial/create_entry",
        data={
            "financial_entry_type": "INVALID",
            "financial_entry_total_amount": "1000.00",
            "financial_entry_description": "Teste",
            "financial_installment_amount": "1000.00",
            "financial_installment_due_date": "2026-12-10",
        },
    )

    assert response.status_code == 200

    with app.app_context():
        assert FinancialEntry.query.count() == 0
        assert FinancialInstallment.query.count() == 0


def test_create_financial_entry_invalid_total_amount(app, client):
    with app.app_context():
        user = create_test_user()

    authenticate_client(client, user)

    response = client.post(
        "/financial/create_entry",
        data={
            "financial_entry_type": "PAYABLE",
            "financial_entry_total_amount": "invalid",
            "financial_entry_description": "Teste",
            "financial_installment_amount": "1000.00",
            "financial_installment_due_date": "2026-12-10",
        },
    )

    assert response.status_code == 200

    with app.app_context():
        assert FinancialEntry.query.count() == 0
        assert FinancialInstallment.query.count() == 0


def test_create_financial_entry_invalid_installment_amount(app, client):
    with app.app_context():
        user = create_test_user()

    authenticate_client(client, user)

    response = client.post(
        "/financial/create_entry",
        data={
            "financial_entry_type": "PAYABLE",
            "financial_entry_total_amount": "1000.00",
            "financial_entry_description": "Teste",
            "financial_installment_amount": "invalid",
            "financial_installment_due_date": "2026-12-10",
        },
    )

    assert response.status_code == 200

    with app.app_context():
        assert FinancialEntry.query.count() == 0
        assert FinancialInstallment.query.count() == 0


def test_create_financial_entry_invalid_due_date(app, client):
    with app.app_context():
        user = create_test_user()

    authenticate_client(client, user)

    response = client.post(
        "/financial/create_entry",
        data={
            "financial_entry_type": "PAYABLE",
            "financial_entry_total_amount": "1000.00",
            "financial_entry_description": "Teste",
            "financial_installment_amount": "1000.00",
            "financial_installment_due_date": "invalid-date",
        },
    )

    assert response.status_code == 200

    with app.app_context():
        assert FinancialEntry.query.count() == 0
        assert FinancialInstallment.query.count() == 0


def test_create_financial_entry_installment_total_mismatch(app, client):
    with app.app_context():
        user = create_test_user()

    authenticate_client(client, user)

    response = client.post(
        "/financial/create_entry",
        data={
            "financial_entry_type": "PAYABLE",
            "financial_entry_total_amount": "1000.00",
            "financial_entry_description": "Teste",
            "financial_installment_amount": "500.00",
            "financial_installment_due_date": "2026-12-10",
        },
    )

    assert response.status_code == 200

    with app.app_context():
        assert FinancialEntry.query.count() == 0
        assert FinancialInstallment.query.count() == 0


def test_create_financial_entry_requires_login(client):
    response = client.get("/financial/create_entry")

    assert response.status_code == 302
    assert "/login" in response.location
