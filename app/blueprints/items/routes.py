# This file is for all the routes related to Items

# Imports
from flask import request, jsonify
from app.blueprints.items import items_bp
from app.blueprints.items.schemas import item_schema, items_schema
from marshmallow import ValidationError
from app.models import  db, Item
from sqlalchemy import select


# New Item
@items_bp.route("/", methods=['POST'])
def create_item():
    try: 
		# Deserialize and validate input data
        item_data = item_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
	# use data to create an instance of Item
    new_item = Item(item_name=item_data['item_name'], price=item_data['price'])
    
	# save new_item to the database and commit changes
    db.session.add(new_item)
    db.session.commit()

	# Use schema to return the serialized data of the created item
    return item_schema.jsonify(new_item), 201

# Get Items(all) Route
@items_bp.route('/', methods=['GET'])
def get_items():
    query = select(Item) # create query to get all items data
    result = db.session.execute(query).scalars().all() # execute query and assign items data to variable
    return items_schema.jsonify(result), 200 # return items data to user display

# Get Item(single) Route
@items_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    query = select(Item).where(Item.id == item_id) # create query to get item data
    item = db.session.execute(query).scalars().first() # execute query and assign item data to variable
    
    # if no item return message to user
    if item == None:
        return jsonify({"message": "invalid item id"}), 400
    
    # if item return item
    return item_schema.jsonify(item), 200
    
# Update Item Route
@items_bp.route('/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    query = select(Item).where(Item.id == item_id) # create query to get item data
    item = db.session.execute(query).scalars().first() # execute query and assign item data to variable
    
    # if no item return message to user
    if item == None:
        return jsonify({"message": "invalid item id"})

    # if item assign item data to variable
    try: 
        item_data = item_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in item_data.items(): # iterating through item data 
        setattr(item, field, value) # assigning item data to attributes

    db.session.commit() # commit changes to database
    return item_schema.jsonify(item), 200

# Delete Item Route
@items_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    query = select(Item).where(Item.id == item_id) # create query to get item data
    item = db.session.execute(query).scalars().first() # execute query and assign item data to variable

    db.session.delete(item) # execute query to delete item
    db.session.commit() # commit changes to database
    return jsonify({"message": f"succesfully deleted user {item_id}"})


