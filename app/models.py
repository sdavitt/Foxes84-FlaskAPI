# This models.py file is responsible for everything database
# Primarily the instantiation of our ORM and the creation of our database models (aka tables/entities)

# import our orm
from flask_sqlalchemy import SQLAlchemy
# create the instance of our ORM (object relational mapper aka translator between python and SQL)
db = SQLAlchemy()

# tools for our models
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash
from uuid import uuid4

#import our LoginManager + tools
from flask_login import LoginManager, UserMixin
# create the instance of our login manager
login = LoginManager()

# necessary function for our login manager
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# create our database model - essentially the python code for a SQL create table
class User(db.Model, UserMixin):
    # lay out our columns just like we would in a SQL create table query
    # column_name = db.Column(db.DataType(<options>), constraints)
    id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password = db.Column(db.String(250), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __init__(self, username, email, password, first_name='', last_name=''):
        self.username = username
        self.email = email.lower()
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password)
        self.id = str(uuid4())