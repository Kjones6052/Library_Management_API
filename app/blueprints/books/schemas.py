# This file is for the schemas associated with Books

# Imports
from app.extensions import ma
from app.models import Book


# schema for Book
class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book # basing schema on the table model for Book


# instantiating schemas
book_schema = BookSchema()
books_schema = BookSchema(many=True)