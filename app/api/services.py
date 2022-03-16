# additional custom made tools for our api
from flask import request, jsonify
from app.models import User
from functools import wraps

# general structure of a custom decorator:
# outer fuction - name of the custom decorator
    # wraps
    # inner function
        # stuff to run before decorated function runs
        # returns decorated function
    # returns inner function

def token_required(api_route):
    @wraps(api_route)
    def decorator_function(*args, **kwargs):
        # code here will run before the decorated route runs
        # get the api token from the request headers
        token = request.headers.get('x-access-token')
        # if there is no token, stop the request from going through and send them a forbidden response
        if not token:
            return jsonify({'Access denied': 'No API token provided - please register an account and request an API token.'}), 401
        # otherwise a token was provided but might not be valid
        if not User.query.filter_by(api_token=token).first():
            return jsonify({'Access denied': 'Invalid API token - please register an account and request an API token.'}), 403
        return api_route(*args, **kwargs)
    return decorator_function