from enum import Enum
from app.extensions import db
from datetime import datetime, timezone
from sqlalchemy import CheckConstraint


class FinancialEntryType(Enum):
    RECEIVABLE = "RECEIVABLE"
    PAYABLE = "PAYABLE"


class FinancialEntry(db.Model):

    __table_args__ = (
        CheckConstraint("total_amount > 0", name="total_amount_check"),
    )

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(FinancialEntryType, name="financial_entry_type"), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime(),
                           nullable=False,
                           default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    #ROM
    user = db.relationship("User", back_populates="financial_entries")
    financial_installments = db.relationship("FinancialInstallment", back_populates="financial_entry")
