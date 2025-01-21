# This file is for linking blueprints and routes

# Import Blueprint and instantiate
from flask import Blueprint
orders_bp = Blueprint('orders_bp', __name__)

# Import routes
from . import routes