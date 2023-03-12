from ..database import db


class ExpenseModel(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    category = db.relationship('CategoryModel', back_populates='expenses', lazy='dynamic')
