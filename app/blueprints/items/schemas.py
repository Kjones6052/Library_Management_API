# This file is for the schemas related to Items

# Imports
from app.models import Item
from app.extensions import ma

# Item Schema
class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item # basing schema on Item Table Model
    
# Instantiating Schema(s)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
