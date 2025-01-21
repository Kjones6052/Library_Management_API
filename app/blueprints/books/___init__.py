# this file is for the blueprint for Books

# imports
from flask import Blueprint

# creating blueprint for books
books_bp = Blueprint('books_bp', __name__)

from . import routes # importing routes for blueprint

