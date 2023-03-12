from ..database import db


class CategoryModel(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)
    expenses = db.relationship('ExpenseModel', back_populates='categories', lazy='dynamic')
