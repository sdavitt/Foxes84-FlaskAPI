# set up and organize the applications general configuration
# what secret variables does it need (secret key, database info, mailer info, api keys, etc.)
# what does it's file structure look like?

# we're gonna get a little help from the os package
import os

# set up the base directory of the entire application - aka help our computer figure out our file system and where to find the different pieces of this project
basedir = os.path.abspath(os.path.dirname(__name__))

# config variables setup
class Config:
    """
    set configuration variables for our entire flask app
    """
    FLASK_APP = os.environ.get('FLASK_APP') # go get the FLASK_APP value from .env
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False