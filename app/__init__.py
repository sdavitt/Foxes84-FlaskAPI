# imports at the top of any necessary modules/files/classes/packages/functions - whatever we need from other files for this file to work
# from the flask package import the Flask object/class
from flask import Flask
# from our config file import the Config class that we created
from config import Config

# import blueprints
from .auth.routes import auth

# imports for database stuff
from .models import db
from flask_migrate import Migrate

# define/instantiate our Flask object... aka tell the computer that this is a flask app
app = Flask(__name__)

# tell this app how it should be configured - over to the config.py file to set up for this!
app.config.from_object(Config)
# aka configure our flask app from the Config object we just wrote

# create link of communication between blueprints and app
# aka register the blueprints
app.register_blueprint(auth)

# set up our ORM and Migrate connections
db.init_app(app)
migrate = Migrate(app, db)

# our flask app is dumb! we need to tell it if any routes or models exist!
# import the routes file here (must be after the definition and config of app)
from . import routes # from the app folder (that we're currently in) import the routes file
from . import models # from the app folder import the routes file