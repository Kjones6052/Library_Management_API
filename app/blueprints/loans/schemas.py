# This file is for schemas related to Loans

# Imports
from app.extensions import ma
from app.models import Loan
from marshmallow import fields


# schema for Loan
class LoanSchema(ma.SQLAlchemyAutoSchema):
    books = fields.Nested("BookSchema", many=True)
    member = fields.Nested("MemberSchema")
    class Meta:
        model = Loan
        fields= ("book_ids", "loan_date", "member_id", "books", "member", "id")


# schema to edit Loan
class EditLoanSchema(ma.Schema):
    add_book_ids = fields.List(fields.Int(), required=True)
    remove_book_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_book_ids", "remove_book_ids")


# instantiating schemas
loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)
return_loan_schema = LoanSchema(exclude=["member_id"])
edit_loan_schema = EditLoanSchema()