# This file is for all the routes related to Members

# Imports
from flask import request, jsonify
from app.blueprints.members import members_bp
from app.blueprints.members.schemas import member_schema, members_schema, login_schema
from marshmallow import ValidationError
from app.models import Member, db
from sqlalchemy import select
from app.extensions import limiter
from app.utils.util import encode_token, token_required


# User Login Route
@members_bp.route("/login", methods=["POST"])
def login():

    # get credentials and assign to variables
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']

    # if error display to user
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Member).where(Member.email == email) # create query to get member data
    member = db.session.execute(query).scalars().first() # execute query and assign member data to variable

    # if member & password are correct encode token for member
    if member and member.password == password:
        token = encode_token(member.id)

        # define successful user message
        response = {
            "status": "success",
            "message": "successfully logged in",
            "token": token
        }

        return jsonify(response), 200 # return successful user message to user display
    else:
        return jsonify({"message": "invalid email or password"}), 400 # if error diplay to user


# New Member
@members_bp.route("/", methods=['POST'])
@limiter.limit("3 per hour") # Limits user to 3 calls per hour on this route only
def create_member():
    try: 
		# Deserialize and validate input data
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
	# use data to create an instance of Member
    new_member = Member(name=member_data['name'], email=member_data['email'], DOB=member_data['DOB'], password=member_data['password'])
    
	# save new_member to the database and commit changes
    db.session.add(new_member)
    db.session.commit()

	# Use schema to return the serialized data of the created member
    return member_schema.jsonify(new_member), 201

# Get Members(all) Route
@members_bp.route('/', methods=['GET'])
def get_members():
    query = select(Member) # create query to get all members data
    result = db.session.execute(query).scalars().all() # execute query and assign members data to variable
    return members_schema.jsonify(result), 200 # return members data to user display

# Get Member(single) Route
@members_bp.route('/<int:member_id>', methods=['GET'])
def get_member(member_id):
    query = select(Member).where(Member.id == member_id) # create query to get member data
    member = db.session.execute(query).scalars().first() # execute query and assign member data to variable
    
    # if no member return message to user
    if member == None:
        return jsonify({"message": "invalid member id"}), 400
    
    # if member return member
    return member_schema.jsonify(member), 200
    
# Update Member Route
@members_bp.route('/<int:member_id>', methods=['PUT'])
@token_required # applying token verification wrapper to route
def update_member(member_id):
    query = select(Member).where(Member.id == member_id) # create query to get member data
    member = db.session.execute(query).scalars().first() # execute query and assign member data to variable
    
    # if no member return message to user
    if member == None:
        return jsonify({"message": "invalid member id"}), 400

    # if member assign member data to variable
    try: 
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in member_data.items(): # iterating through member data 
        setattr(member, field, value) # assigning member data to attributes

    db.session.commit() # commit changes to database
    return member_schema.jsonify(member), 200

# Delete Member Route
@members_bp.route('/<int:member_id>', methods=['DELETE'])
@token_required # applying token verification wrapper to route
def delete_member(member_id):
    query = select(Member).where(Member.id == member_id) # create query to get member data
    member = db.session.execute(query).scalars().first() # execute query and assign member data to variable

    db.session.delete(member) # execute query to delete member
    db.session.commit() # commit changes to database
    return jsonify({"message": f"succesfully deleted user {member_id}"}), 200


