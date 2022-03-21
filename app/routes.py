# flask routes control what content is shown on what url depending on how the user is accessing that url, what button they've pressed, etc.

# the general structure of a flask route is a function with a decorator
# a decorator adds lines of code that run before and after the decorated function

# our first route:
# goal display the index.html file when use navigates to the base url aka 'http://127.0.0.1:5000/'

# in order to do this we need a few tools
# 1. we need access to our app
from flask_login import login_required
from app import app # import the app variable defined in __init__.py
# 2. we need the ability to show an html file at a specified url
    # render_template function
    # if your route's job is to display an html page -> it's return value should be a call to render_template
from flask import render_template, request
from .forms import DriverForm

# non-flask imports for route functionality
from random import choice
import requests as r
from .services import getActorImages # .services says "from the services file" rather than "from the services module"

@app.route('/') # decorator says: this function is a route of the flask app 'app' with the url endpoint '/'
def home():
    print('Hello, Foxes!')
    x = choice(['Patrick','Elif','Amir','Cameron','Kyle','Brandt','Brandon','Devon'])
    print(f'X has value {x}. This value will be passed into render_template as a keyword argument and the keyword used in a jinja expression in index.html')
    return render_template('index.html', name=x)


# a second route!
@app.route('/mcfc')
@login_required
def mancity():
    context = {
        'headline': 'Manchester City beat Sporting Lisbon in the Champions League Round of 16!',
        'mcfcg': 5,
        'slg': 0,
        'favorites': {'Joao Cancelo': 27, 'Ederson': 1, 'Fernandinho': 25, 'Phil Foden': 47, 'Kevin De Bruyne': 17},
        'manager': 'Pep Guardiola'
    }
    return render_template('soccer.html', **context)


# gallery route
@app.route('/actors')
@login_required
def gallery():
    actors = getActorImages()
    #print(actors)
    return render_template('gallery.html', actors=actors, welcomeback='Lamont')

# f1 driver info route
# methods specify the acceptable methods of connection to this endpoint on our server
    # methods defaults to just 'GET'
@app.route('/f1', methods=['GET', 'POST'])
def f1drivers():
    form = DriverForm() # this form will be used in both the GET and POST sides of this route
    # 2 scenarios here:
        # 1. User is just accessing this page
            # GET - getting data from the web server
        # 2. User has submitted the form requesting certain driver information
            # POST - sending data to the web server
    if request.method == 'POST':
        # this means the user has submitted the form
        # Two possible behaviors
            # user provided good form info (aka a real driver name)
        data = r.get(f'https://ergast.com/api/f1/drivers/{form.drivername.data}.json').json()
        if data['MRData']['total'] != '0':
            # make api request and display relevant info
            driver = data['MRData']['DriverTable']['Drivers'][0]
        else:
            # user provided bad form info
            driver = form.drivername.data
        # return a render_template with the relevant or lack of relevant driver data
        return render_template('f1drivers.html', form=form, driver=driver) # after POST
    return render_template('f1drivers.html', form=form, driver=None) # works for our GET requests