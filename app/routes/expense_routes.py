from flask.views import MethodView
from flask_smorest import Blueprint, abort
from http import HTTPStatus
from ..schemas import Expense
from ..models import ExpenseModel
from ..database import db
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('expenses', __name__, description="operations on db", url_prefix="/expenses")


@bp.route("/")
class Expenses(MethodView):

    @bp.response(HTTPStatus.ACCEPTED, Expense(many=True))
    def get(self):
        return ExpenseModel.query.all()

    @bp.arguments(Expense)
    def post(self, expense_data):
        expense = ExpenseModel(**expense_data)

        try:
            db.session.add(expense)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(HTTPStatus.BAD_REQUEST, e)

        return HTTPStatus.CREATED, "entry created"


@bp.route("<int:_id>")
class ExpenseByID(MethodView):

    @bp.response(HTTPStatus.ACCEPTED, Expense)
    def get(self, _id):
        return ExpenseModel.query.get_or_404(_id)

    @bp.arguments(Expense)
    def put(self, expense_data, _id):
        old_expense = ExpenseModel.query.get_or_404(_id)
        if old_expense:
            old_expense.name = expense_data['name']
            old_expense.description = expense_data['description']
            old_expense.amount = expense_data['amount']
        else:
            old_expense = ExpenseModel(**expense_data)
        db.session.add(old_expense)
        db.session.commit()

        return HTTPStatus.CREATED, "updated entry"

    @bp.response(HTTPStatus.CREATED, Expense)
    def delete(self, _id):
        item = ExpenseModel.query.get_or_404(_id)

        db.session.delete(item)
        db.session.commit()
        return item
