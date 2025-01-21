# This file is for all the routes related to Orders

# Imports
from flask import request, jsonify
from app.blueprints.orders import orders_bp
from app.blueprints.orders.schemas import order_schema, orders_schema, create_order_schema, receipt_schema
from marshmallow import ValidationError
from app.models import  db, Order, OrderItems
from sqlalchemy import select
from datetime import date



@orders_bp.route("/", methods=["POST"])
def create_order():
    try:
        order_data = create_order_schema.load(request.json) # creating variable with the schema format
        print(order_data)
    except ValidationError as e:
        return jsonify(e.messages), 400 # if error return message to user display

    new_order = Order(member_id=order_data['member_id'], order_date=date.today()) # creating a new Order object

    db.session.add(new_order) # adding new order to database
    db.session.commit() # commit changes to database so we can access it

    for item in order_data['item_quantity']:# looping through each item in the order
        order_item = OrderItems(order_id=new_order.id, item_id=item['item_id'], quantity=item['item_quantity']) # get item data and assign to variable
        db.session.add(order_item) # add item to order

    db.session.commit() # commit changes to database

    total = 0 # setting total to 0
    for order_item in new_order.order_items: # looping through each item in the order
        price = order_item.quantity * order_item.item.price # getting total price (quantity * price)
        total += price # adding total price to total for new value

    # create receipt using variables from above
    receipt = {
        "total": total,
        "order": new_order
    }

    # return receipt to user according to receipt schema
    return receipt_schema.jsonify(receipt)