# initial blueprint setup
from flask import Blueprint, jsonify, request

api = Blueprint('api', __name__, url_prefix='/api')

# imports for api routes
from app.models import db, Animal
from .services import token_required


# the route decorator belonging to a blueprint starts with @<blueprint_name> rather than @app
@api.route('/test')
def test():
    # jsonify? transforms python dictionary (or list) into json data
    return jsonify({'datadatadata': 'whoa this is some cool data'}), 200

# route for getting all animals
@api.route('/animals', methods=['GET'])
def getAnimals():
    """
    [GET] return json data on all of the animals in our database
    """
    # query the animals
    # I want to jsonify the result of .to_dict() for each animal in our animals query
    animals = {'Animals': [a.to_dict() for a in Animal.query.all()]}
    # jsonify and send
    return jsonify(animals), 200

# route for getting one animal - our first dynamic route
# the function for this route will expect input coming through the url
@api.route('/animal/name/<string:name>', methods=['GET'])
def getAnimal(name):
    """
    [GET] that accepts an animal name through the url and either gets the appropriate animal from our database
    or returns that we don't have that animal
    """
    a = Animal.query.filter_by(name=name.title()).first()
    if a:
        return jsonify(a.to_dict()), 200
    else:
        return jsonify({'Request failed': 'No animal with that name.'}), 404

# route for creating a new animal
@api.route('/create/animal', methods=['POST'])
@token_required
def createAnimal():
    """
    [POST] creates a new animal in our database with data provided in the request body
    expected data format: JSON:
        {
            'name': <str>,
            'sci_name': <str>,
            'description': <str>,
            'price': <float>,
            'image': <str>,
            #### rest of k:v pairs optional
            'size': <str>,
            'weight': <int>,
            'diet': <str>,
            'habitat': <str>,
            'lifespan': <int>,
            'inventory': <int>
        }
    """
    # grab any json data from the body of the request made to this route
    # depending on how specific we want our data to be - we may want to build out some checks on the data coming in
    # does it actually make sense? is it something we want in our database?
    # otherwise, create the new animal in the database
    try:
        data = request.get_json()
        new_animal = Animal(data)
        db.session.add(new_animal)
        db.session.commit()
        return jsonify({'Created New Animal': new_animal.to_dict()}), 201
    except:
        return jsonify({'Create Animal Rejected': 'Animal already exists or improper request.'}), 400


# route for updating an animal
@api.route('/animal/update/<string:id>', methods=['PUT']) # PUT is used for updating existing data - just like POST, PUT requests can include data being sent to the web server
@token_required
def updateAnimal(id):
    """
    [PUT] accepts an animal ID in the URL and JSON data in the PUT request body in the following format (all values optional):
        {
            'name': <str>,
            'sci_name': <str>,
            'description': <str>,
            'price': <float>,
            'image': <str>,
            'size': <str>,
            'weight': <int>,
            'diet': <str>,
            'habitat': <str>,
            'lifespan': <int>,
            'inventory': <int>
        }
    """
    try:
        # grab the request body and query the database for an animal with that ID
        animal = Animal.query.get(id)
        data = request.get_json()
        # then update the animal object
        animal.from_dict(data)
        # and recommit it to the database aka save changes to the DB
        db.session.commit()
        return jsonify({'Updated animal': animal.to_dict()}), 200
    except:
        return jsonify({'Request failed': 'invalid body or animal ID'}), 400

# route for deleting an animal
@api.route('/animal/remove/<string:id>', methods=['DELETE'])
@token_required
def removeAnimal(id):
    """
    [DELETE] accepts an animal ID - if that ID exists in the database, remove that animal from the database
    """
    # check if that animal exists
    animal = Animal.query.get(id)
    if not animal: # if no animal with that id is in the database
        # tell the user remove failed
        return jsonify({'Remove failed': 'No animal of that ID in the database.'}), 404
    db.session.delete(animal)
    db.session.commit()
    return jsonify({'Removed animal': animal.to_dict()}), 200


@api.route('/inventoryupdate', methods=['POST'])
def updateInventory():
    """
    accept an order and reduce inventory accordingly
    incoming data: {
        animals: {
            <id>: {
                data: {...},
                quantity: <int>
            }
        },
        size: <int>,
        total: <float>
    }
    loop through the animals key accessing the id and the quantity
    """
    data = request.get_json()
    for id in data['animals']:
        a = Animal.query.get(id)
        a.inventory = a.inventory - data['animals'][id]['quantity']
        if a.inventory < 0:
            return jsonify({'Inventory Issue': f'not enough inventory of {a.name}'}), 500
    db.session.commit()
    return jsonify({'Inventory': 'update complete'}), 200
