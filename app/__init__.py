# This file is responsible for creating the application instance

# Imports
from flask import Flask
from app.models import db
from app.extensions import ma, limiter, cache
from app.blueprints.members import members_bp
from app.blueprints.books import books_bp
from app.blueprints.loans import loan_bp
from app.blueprints.items import items_bp
from app.blueprints.orders import orders_bp
from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml'  # Our API URL (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Your API's Name"
    }
)

# Create App Instance
def create_app(config_name):

    app = Flask(__name__) # activating flask
    app.config.from_object(f'config.{config_name}') # activating specified config

    # Add extensions to app
    db.init_app(app)  # for database operations
    ma.init_app(app) # for use of marshmallow
    limiter.init_app(app) # to limit requests for security
    cache.init_app(app) # to cache data for faster response times

    # Registering blueprints
    app.register_blueprint(members_bp, url_prefix='/members')
    app.register_blueprint(books_bp, url_prefix='/books')
    app.register_blueprint(loan_bp, url_prefix='/loans')
    app.register_blueprint(items_bp, url_prefix='/items')
    app.register_blueprint(orders_bp, url_prefix='/oreders')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL) #Registering our swagger blueprint


    return app