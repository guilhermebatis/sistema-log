from enum import Enum
from app.extensions import db
from sqlalchemy import CheckConstraint


class StatusFinancialInstallment(Enum):
    PENDING = "PENDING"
    PAID = "PAID"


class FinancialInstallment(db.Model):

    __table_args__ = (
        CheckConstraint("amount > 0", name="amount_check"),
    )

    id = db.Column(db.Integer, primary_key=True)
    financial_entry_id = db.Column(db.Integer, db.ForeignKey('financial_entry.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum(StatusFinancialInstallment), nullable=False)
    due_date = db.Column(db.Date, nullable=False)

    #ROM
    financial_entry = db.relationship("FinancialEntry", back_populates="financial_installments",)
    financial_payment = db.relationship("FinancialPayment", back_populates="financial_installment",)
