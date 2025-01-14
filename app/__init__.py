# This file is responsible for creating the application instance

# Imports
from flask import Flask
from app.models import db # Absolute Path (start from app folder)
# from .models import db # Relative Path (start from current location)
from app.extensions import ma
from app.blueprints.members import members_bp

# Create App Instance
def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    # Add extensions to app
    db.init_app(app) 
    ma.init_app(app)

    # Registering blueprints
    app.register_blueprint(members_bp, url_prefix='/members')


    return app