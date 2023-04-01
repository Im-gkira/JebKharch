from flask import Flask, jsonify
from flask_smorest import Api
from app.database import db
from app.config import Config
from app.routes import ExpenseBlueprint, CategoryBlueprint, AuthBlueprint
from flask_jwt_extended import JWTManager
from app.models import BlockedJWT
from flask_migrate import Migrate
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)

    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return BlockedJWT.query.get(jwt_payload['jti']).first()

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    api = Api(app)
    api.register_blueprint(ExpenseBlueprint)
    api.register_blueprint(CategoryBlueprint)
    api.register_blueprint(AuthBlueprint)

    return app


if __name__ == '__main__':
    create_app()
