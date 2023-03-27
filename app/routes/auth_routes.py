from flask.views import MethodView
from flask_smorest import Blueprint, abort
from http import HTTPStatus
from ..schemas import User
from ..models import UserModel, BlockedJWT
from ..database import db
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, get_jwt_identity

bp = Blueprint("auth", __name__, description="auth related operations")


@bp.route("/register")
class Register(MethodView):

    @bp.arguments(User)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.email == user_data['email']).first()

        if user:
            abort(HTTPStatus.ALREADY_REPORTED, "user already exists")

        user_data['password'] = pbkdf2_sha256.hash(user_data['password'])
        user = UserModel(**user_data)

        db.session.add(user)
        db.session.commit()

        return HTTPStatus.CREATED, "Registered Successfully"


@bp.route("/login")
class Login(MethodView):

    @bp.arguments(User)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.email == user_data["email"]).first()

        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, HTTPStatus.ACCEPTED

        abort(HTTPStatus.UNAUTHORIZED, message="Invalid Credentials")


@bp.route("/logout")
class Logout(MethodView):

    @bp.response(HTTPStatus.OK, User)
    def get(self):
        jwt_id = get_jwt_identity()

        blocked_jwt = BlockedJWT(token=jwt_id)

        db.session.add(blocked_jwt)
        db.session.commit()

        return {"message": "logged out successfully"}, HTTPStatus.OK
