# This models.py file is responsible for everything database
# Primarily the instantiation of our ORM and the creation of our database models (aka tables/entities)

# import our orm
from flask_sqlalchemy import SQLAlchemy

# create the instance of our ORM (object relational mapper aka translator between python and SQL)
db = SQLAlchemy()

# create our database model - essentially the python code for a SQL create table
class User(db.Model):
    # lay out our columns just like we would in a SQL create table query
    # column_name = db.Column(db.DataType(<options>), constraints)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)