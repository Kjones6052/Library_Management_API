# This file is used to run the app

# Imports
from app import create_app
from app.models import db

# Activating app with specified config
app = create_app('DevelopmentConfig') 

with app.app_context():
    db.drop_all() # Drops all tables in database (commented out for later use if needed)
    db.create_all() # Creates all tables based on models

# Run App
app.run()