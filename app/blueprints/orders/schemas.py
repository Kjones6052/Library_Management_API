# This file is for the schemas related to Orders

# Imports
from app.models import Order, OrderItems
from app.extensions import ma
from marshmallow import fields


# Receipt Schema
class ReceiptSchema(ma.Schema):
    total = fields.Int(required=True)
    order = fields.Nested("OrderSchema")


# Order Schema
class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order # basing schema on Order Table Model
        include_relationships = True
    order_items = fields.Nested("OrderItemSchema", exclude=["id"], many=True)


# Order Item Schema
class OrderItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItems
    item = fields.Nested("ItemSchema", exclude=["id"])


# Create Order Schema
class CreateOrderSchema(ma.Schema):
    member_id = fields.Int(required=True)
    item_quantity = fields.Nested("ItemQuantity", many=True)


# Item Quantity Schema
class ItemQuantitySchema(ma.Schema):
    item_id = fields.Int(required=True)
    item_quantity = fields.Int(required=True)

    
# Instantiating Schema(s)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
create_order_schema = CreateOrderSchema()
receipt_schema = ReceiptSchema()
