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

# import choice for our random behaviour
from random import choice

@app.route('/') # decorator says: this function is a route of the flask app 'app' with the url endpoint '/'
def home():
    print('Hello, Foxes!')
    x = choice(['Patrick','Elif','Amir','Cameron','Kyle','Brandt','Brandon','Devon'])
    print(f'X has value {x}. This value will be passed into render_template as a keyword argument and the keyword used in a jinja expression in index.html')
    return render_template('index.html', name=x)


# a second route!
@app.route('/mcfc')
def mancity():
    headline = 'Manchester City beat Sporting Lisbon in the Champions League Round of 16!'
    mcgoals = 'Five'
    sportinggoals = 0
    return render_template('soccer.html', headline=headline, mcfcg=mcgoals, slg=sportinggoals)