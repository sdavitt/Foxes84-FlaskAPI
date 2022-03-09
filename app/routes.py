# flask routes control what content is shown on what url depending on how the user is accessing that url, what button they've pressed, etc.

# the general structure of a flask route is a function with a decorator
# a decorator adds lines of code that run before and after the decorated function

# our first route:
# goal display the index.html file when use navigates to the base url aka 'http://127.0.0.1:5000/'

# in order to do this we need a few tools
# 1. we need access to our app
from app import app # import the app variable defined in __init__.py
# 2. we need the ability to show an html file at a specified url
    # render_template function
    # if your route's job is to display an html page -> it's return value should be a call to render_template
from flask import render_template

@app.route('/') # decorator says: this function is a route of the flask app 'app' with the url endpoint '/'
def home():
    print('Hello, Foxes!')
    x = 5
    print(f'X has value {x}. This will print in the terminal when this function runs when the url endpoint / is accessed.')
    return render_template('index.html')


# a second route!
@app.route('/mcfc')
def mancity():
    x = 'Manchester City'
    print(f'X has value {x}. This will print in the terminal when this function runs when the url endpoint /mcfc is accessed.')
    return render_template('soccer.html')