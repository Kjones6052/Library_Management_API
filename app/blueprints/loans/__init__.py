# This file is for the Loan Blueprint

# Imports
from flask import Blueprint


# Loan Blueprint
loan_bp = Blueprint('loan_bp', __name__)

from . import routes # importing routes for blueprint