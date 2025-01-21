# This file is for the schemas related to Members

# Imports
from app.models import Member
from app.extensions import ma

# Member Schema
class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member # basing schema on Member Table Model
    
# Instantiating Schema(s)
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

# Creating a login schema that excludes details name, DOB for member authentication
login_schema = MemberSchema(exclude=['name', 'DOB'])