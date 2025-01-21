# This file is for all routes associated with Loans

# Imports
from flask import jsonify, request
from . import loan_bp
from .schemas import loan_schema, loans_schema, return_loan_schema, edit_loan_schema
from app.models import db, Book, Loan
from sqlalchemy import select
from marshmallow import ValidationError


# Create Loan Route
@loan_bp.route("/", methods=["POST"])
def create_loan():
    try:
        loan_data = loan_schema.load(request.json) # validate loan data according to schema
        print(loan_data) # display data in terminal
    except ValidationError as e: # if error return message to user
        return jsonify(e.messages), 400
    
    # creating a new loan object and assigning it to a variable
    new_loan = Loan(loan_date=loan_data['loan_date'], member_id=loan_data["member_id"])

    for book_id in loan_data["book_ids"]: # for each book id in the list
        query = select(Book).where(Book.id == book_id) # create query get book according to book id
        book = db.session.execute(query).scalar() # execute query and assign data to variable

        # if book ad to list of books for loan
        if book:
            new_loan.books.append(book)
        else:
            return jsonify({"message": "invalid book id"}), 400
        
    db.session.add(new_loan) # adding loan to database
    db.session.commit() # commiting changes to database

    return return_loan_schema.jsonify(new_loan), 201


# Get Loans Route
@loan_bp.route("/", methods=['GET'])
def get_loans():
    query = select(Loan) # create query to get loans
    result = db.session.execute(query).scalars().all() # execute query and assign data to variable
    return loans_schema.jsonify(result), 200 # return loans to user display


# Delete Loan Route
@loan_bp.route("/<int:loan_id>", methods=['DELETE'])
def delete_loan(loan_id):
    query = select(Loan).where(Loan.id == loan_id) # create query to get loan according to id
    loan = db.session.execute(query).scalars().first() # execute query and assign to variable

    db.session.delete(loan) # delete loan from database
    db.session.commit() # commit changes to database

    return jsonify({"message": f"succesfully deleted loan {loan_id}"}), 200
    

# Update Loan Route
@loan_bp.route("/<int:loan_id>", methods=['PUT'])
def edit_loan(loan_id):
    try:
        loan_edits = edit_loan_schema(request.json) # creating instance of edit loan schema
    except ValidationError as e:
        return jsonify(e.messages), 400 # if error return message to user display

    query = select(Loan).where(Loan.id == loan_id) # create query to get loan according to id
    loan = db.session.execute(query).scalars().first() # execute query and assign to variable

    for book_id in loan_edits['add_book_ids']: # for each book id input
        query = select(Book).where(Book.id == book_id) # create query to get book according to id
        book = db.session.execute(query).scalars().first() # execute query and assign to variable

        # if there is a book and it's not in the loan already add book to loan
        if book and book not in loan.books: 
            loan.books.append(book)

    for book_id in loan_edits['remove_book_ids']: # for each book id input
        query = select(Book).where(Book.id == book_id) # create query to get book according to id
        book = db.session.execute(query).scalars().first() # execute query and assign to variable

        # if there is a book and it is in the loan remove book from loan
        if book and book in loan.books:
            loan.books.remove(book)

    db.session.commit() # commit changes to database
    return return_loan_schema.jsonify(loan)

