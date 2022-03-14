# our auth system here is designed to be a subsection of our larger flask app
# we need to connect it to our larger flask app so we define it as a blueprint
from flask import Blueprint, render_template, request, redirect, url_for, flash
# define our blueprint/create the auth instance of a flask blueprint
auth = Blueprint('auth', __name__, template_folder='auth_templates', url_prefix='/auth')

# import forms
from .authforms import SignInForm, RegisterForm

# make my first route in the auth blueprint
@auth.route('/', methods=['GET', 'POST'])
def signin():
    siform = SignInForm()
    if request.method == 'POST': # user submitted form
        if siform.validate_on_submit():
            # ok, the user gave us proper form input
            print(siform.data)
            # actually go about signing the user in (more on this tomorrow)
            # successful sign-in - redirect user to homepage
            flash(f'Welcome back, {siform.username.data}!')
            return redirect(url_for('home'))
        else:
            # bad form info - tell them to try again
            flash(f'Login failed, incorrect username or password.')
            return redirect(url_for('auth.signin'))
    return render_template('signin.html', siform=siform)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    rform = RegisterForm()
    if request.method == 'POST': # user submitted form
        if rform.validate_on_submit():
            # ok, the user gave us proper form input
            print(rform.data)
            # actually go about signing the user in (more on this tomorrow)
            # successful registration - redirect user to homepage
            flash(f'Successfully registered! Welcome, {rform.first_name.data}!')
            return redirect(url_for('home'))
        else:
            # bad form info - tell them to try again
            flash('Your passwords did not match or you provided an improper email/username. Try again.')
            return redirect(url_for('auth.register'))
    return render_template('register.html', rform=rform)