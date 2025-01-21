# this file is for all the routes associated with Books

# imports
from flask import jsonify, request
from . import books_bp
from .schemas import book_schema, books_schema
from app.models import db
from app.models import Book
from sqlalchemy import select
from marshmallow import ValidationError
from app.extensions import cache


# create book route
@books_bp.route("/", methods=['POST'])
def create_book():
    try: 
        book_data = book_schema.load(request.json) # validate book data according to schema
    except ValidationError as e:
        return jsonify(e.messages), 400 # if error return message to user display
    
    # creating a book object and assigning it to a variable
    new_book = Book(author=book_data['author'], genre=book_data['genre'], desc=book_data['desc'], title=book_data['title'])
    
    db.session.add(new_book) # adding book object to database
    db.session.commit() # commit changes to database

    return book_schema.jsonify(new_book), 201


# get books(all) route
@books_bp.route("/", methods=['GET'])
# @cache.cached(timeout=60) # cache books data for faster response to repetitive requests
def get_books():
    try:
        page = int(request.args.get('page')) # creating variable for page number
        per_page = int(request.args.get('per_page')) # creating variable for number per page
        query = select(Book) # create query to get all books
        result = db.session.execute(query, page=page, per_page=per_page) # execute query with parameters and assign to variable
        return books_schema.jsonify(result), 200 # return books data to user display according to schema

    except:
        query = select(Book) # create query to get all books
        result = db.session.execute(query).scalars().all() # execute query and assign to variable
        return books_schema.jsonify(result), 200 # return books data to user display according to schema

    

# update book route
@books_bp.route("/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    query = select(Book).where(Book.id == book_id) # create query to get book according to id
    book = db.session.execute(query).scalars().first() # execute query and assign to variable
    
    # if no book return message to user display
    if book == None:
        return jsonify({"message": "invalid book id"})
    
    try: 
        book_data = book_schema.load(request.json) # if book validate data with schema and assign to variable
    except ValidationError as e:
        return jsonify(e.messages), 400 # if error return message to user display
    
    # for each field in the book data, assign values to attributes according to field name
    for field, value in book_data.items():
        setattr(book, field, value)

    db.session.commit() # commit changes to database
    return book_schema.jsonify(book), 200


# delete book route
@books_bp.route("/<int:book_id>", methods=['DELETE'])
def delete_book(book_id):
    query = select(Book).where(Book.id == book_id) # create query to get book according to id
    book = db.session.execute(query).scalars().first() # execute query and assign to variable

    db.session.delete(book) # delete book from database
    db.session.commit() # commit changes to database
    return jsonify({"message": f"succesfully deleted user {book_id}"})
    

# get popular books route
@books_bp.route("/popular", methods=['GET'])
def popular_books():
    query = select(Book)
    books = db.session.execute(query).scalars().all()

    # sorting using lamba function (key= lambda object: how to sort)
    books.sort(key= lambda book: len(book.loans), reverse=True) # sorting books according to number of loans in reverse order

    return books_schema.jsonify(books) # return sorted list of books to user display according to schema


# search book route
@books_bp.route("/search", methods=['GET'])
def search_book():
    title = request.args.get("title") # query database for a book according to title

    query = select(Book).where(Book.title.like(f'%{title}%')) # create query to get book with similar title using .like()
    books = db.session.execute(query).scalars().all() # execute query and assign to variable

    return books_schema.jsonify(books) # return data to use display
