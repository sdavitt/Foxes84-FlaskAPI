# this page is for laying out objects for each of our forms
# these objects will describe the form fields, types of data, and any validators

# imports
from flask_wtf import FlaskForm # the base form object for forms in our flask app
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# class for the form describing the form's structure and datatypes
# this custom class inherits from FlaskForm - it is our customization of the base Form structure from Flask_WTF
class DriverForm(FlaskForm):
    # having done the inheritance we just need to provide the fields that this form will show
    drivername = StringField('Driver Name', validators=[DataRequired()])
    submit = SubmitField()