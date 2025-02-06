# This file is for token creation and validation

# Imports
import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import request, jsonify


# Creating a token signature
SECRET_KEY = "big bad mama jama"

# Funtion to encode token
def encode_token(member_id):
    # Payload = info packaged into token
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1), # Exiration
        'iat': datetime.now(timezone.utc), # Issued At
        'sub': member_id # Member token belongs to
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256") # Creating token
    return token 

# Creating token verification wrapper for routes
def token_required(f): # f represents the function we are wrapping
    @wraps(f) # wrapping the function received with the decoration function below
    def decorated(*args, **kwargs): # adding functions to our wrapper with args and kwargs
        token = None # setting token == nothing

        if 'Authorization' in request.headers: # verifying authorization was requested
            
            # accessing token string using split() to remove 'Bearer' from the string
            token = request.headers['Authorization'].split()[1]

            # if no token return message to user
            if not token:
                return jsonify({'message': 'missing token'}), 400
            
            # verify valid token & get member_id
            try:
                data = jwt.decode(token, SECRET_KEY, algorithm="HS256")
                member_id = data['sub']

            # specified user message for expired token
            except jwt.ExpiredSignatureError as e:
                return jsonify({'message': 'token expired'}), 400
            
            # specified user message for invalid token
            except jwt.InvalidTokenError:
                return jsonify({'message': 'invalid token'}), 400
            
            # return function to wrapper with member_id, args, and kwargs
            return f(*args, **kwargs)
        
        # if token not verified return message to user
        else:
            return jsonify({'message': 'You must be logged in to access this.'}), 400
      
    # return decorated(wrapped) function 
    return decorated