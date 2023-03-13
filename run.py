from flask import Flask
from flask_smorest import Api
from app.database import db
from app.config import Config
from app.routes import ExpenseBlueprint, CategoryBlueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()
    api = Api(app)
    api.register_blueprint(ExpenseBlueprint)
    api.register_blueprint(CategoryBlueprint)

    return app


if __name__ == '__main__':
    create_app()
