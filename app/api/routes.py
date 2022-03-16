# initial blueprint setup
from flask import Blueprint, jsonify

api = Blueprint('api', __name__, url_prefix='/api')

# imports for api routes
from app.models import Animal


# the route decorator belonging to a blueprint starts with @<blueprint_name> rather than @app
@api.route('/test')
def test():
    # jsonify? transforms python dictionary (or list) into json data
    return jsonify({'datadatadata': 'whoa this is some cool data'})

# route for getting all animals
@api.route('/animals', methods=['GET'])
def getAnimals():
    """
    [GET] return json data on all of the animals in our database
    """
    # query the animals
    # I want to jsonify the result of .to_dict() for each animal in our animals query
    animals = [a.to_dict() for a in Animal.query.all()]
    # jsonify and send
    return jsonify(animals)

# route for getting one animal

# route for creating a new animal

# route for updating an animal

# route for deleting an animal