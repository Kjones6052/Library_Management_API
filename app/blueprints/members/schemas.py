# This file is for the schemas related to Members

# Imports
from app.models import Member
from app.extensions import ma

# Member Schema
class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member
    
# Instantiating Schema(s)
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)