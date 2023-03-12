from flask.views import MethodView
from flask_smorest import Blueprint, abort
from http import HTTPStatus
from ..schemas import Category
from ..models import CategoryModel
from ..database import db
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('categories', __name__, description="operations on categories", url_prefix="/categories")


@bp.route("/")
class Categories(MethodView):

    @bp.response(HTTPStatus.ACCEPTED, Category(many=True))
    def get(self):
        return CategoryModel.query.all()

    @bp.arguments(Category)
    @bp.response(HTTPStatus.CREATED, Category)
    def post(self, data):
        category = Category(**data)

        try:
            db.session.add(category)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(HTTPStatus.BAD_REQUEST, e)

        return category


@bp.route("/<int:_id>")
class CategoriesByID(MethodView):

    @bp.response(HTTPStatus.ACCEPTED, Category)
    def get(self, _id):
        return CategoryModel.query.get_or_404(_id)

    @bp.arguments(Category)
    def put(self, data, _id):
        category = CategoryModel.query.get(_id)

        if category:
            category.name = data["name"]
        else:
            category = Category(**data)

        db.session.add(category)
        db.session.commit()
        return HTTPStatus.CREATED, "updated entry"

    @bp.response(HTTPStatus.ACCEPTED, "deleted entry")
    def delete(self, _id):
        category = CategoryModel.query.get(_id)

        db.session.delete(category)
        db.session.commit()

        return HTTPStatus.ACCEPTED, "deleted entry"
