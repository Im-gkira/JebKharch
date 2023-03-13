import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Flask-Smorest Configuration:
        API_TITLE: Title for the API
        API_VERSION: Version of the API
        OPENAPI_VERSION: OpenAPI specification version to use (default is '3.0.3')
        OPENAPI_URL_PREFIX: URL prefix for the generated OpenAPI JSON file

    Database Configuration:
        SQLALCHEMY_DATABASE_URI: Database URI to connect to
        SQLALCHEMY_TRACK_MODIFICATIONS: Set to False to disable tracking modifications on objects and improve performance
    """
    API_TITLE = "Expense Tracker"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("SECRET_KEY","19032098ukhdska")
