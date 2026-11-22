from app.extensions import db

class FinancialPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    financial_installment_id = db.Column(db.Integer,
                                         db.ForeignKey('financial_installment.id'),
                                         nullable=False,
                                         unique=True)
    payment_date = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    #ROM
    financial_installment = db.relationship('FinancialInstallment', back_populates='financial_payment')