# This file is for linking blueprints and routes

# Import Blueprint and instantiate
from flask import Blueprint
items_bp = Blueprint('items_bp', __name__)

# Import routes
from . import routes