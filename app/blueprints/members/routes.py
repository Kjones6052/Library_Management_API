# This file is for all the routes related to Members

# Imports
from flask import request, jsonify
from app.blueprints.members import members_bp
from app.blueprints.members.schemas import member_schema, members_schema
from marshmallow import ValidationError
from app.models import Member, db
from sqlalchemy import select, delete


# New Member
@members_bp.route("/", methods=['POST'])
def create_member():
    try: 
		# Deserialize and validate input data
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
	# use data to create an instance of Member
    new_member = Member(name=member_data['name'], email=member_data['email'], DOB=member_data['DOB'])
    
	# save new_member to the database
    db.session.add(new_member)
    db.session.commit()

	# Use schema to return the serialized data of the created member
    return member_schema.jsonify(new_member), 201

# Get Members (all)
@members_bp.route('/', methods=['GET'])
def get_members():
    query = select(Member)
    result = db.session.execute(query).scalars().all()
    return members_schema.jsonify(result), 200 

# Get Member (single)
@members_bp.route('/<int:member_id>', methods=['GET'])
def get_member(member_id):
    query = select(Member).where(Member.id == member_id)
    member = db.session.execute(query).scalars().first()
    
    if member == None:
        return jsonify({"message": "invalid user id"}), 400
    
    return member_schema.jsonify(member), 200
    
# Update Member
@members_bp.route('/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    query = select(Member).where(Member.id == member_id)
    member = db.session.execute(query).scalars().first()
    
    if member == None:
        return jsonify({"message": "invalid user id"})

    try: 
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in member_data.items():
        setattr(member, field, value)

    db.session.commit()
    return member_schema.jsonify(member), 200

# Delete Member
@members_bp.route('/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    query = delete(Member).where(Member.id == member_id)
    member = db.session.execute(query)

    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": f"succesfully deleted user {member_id}"})


