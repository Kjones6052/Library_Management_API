# This file is for linking blueprints and routes

# Import Blueprint and instantiate
from flask import Blueprint
members_bp = Blueprint('members_bp', __name__)

# Import routes
from . import routes