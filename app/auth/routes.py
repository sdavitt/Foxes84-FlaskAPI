# our auth system here is designed to be a subsection of our larger flask app
# we need to connect it to our larger flask app so we define it as a blueprint
from flask import Blueprint, render_template, request, redirect, url_for, flash
# define our blueprint/create the auth instance of a flask blueprint
auth = Blueprint('auth', __name__, template_folder='auth_templates', url_prefix='/auth')

# import forms
from .authforms import SignInForm, RegisterForm
# import user, db, and login stuff
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, login_required, logout_user


# make my first route in the auth blueprint
@auth.route('/', methods=['GET', 'POST'])
def signin():
    siform = SignInForm()
    if request.method == 'POST': # user submitted form
        if siform.validate_on_submit():
            # ok, the user gave us proper form input
            # actually go about signing the user in
            user = User.query.filter_by(username=siform.username.data).first()
            # check if the username exists in the database and check if the password matches
            if user and check_password_hash(user.password, siform.password.data):
                # if everything looks good, sign the user in thru our login manager
                login_user(user)
                print(current_user, current_user.__dict__)
                # successful sign-in - redirect user to homepage
                flash(f'Welcome back, {current_user.first_name}!', category='info')
                return redirect(url_for('home'))
        # bad form info - tell them to try again
        flash(f'Login failed, incorrect username or password.', category='danger')
        return redirect(url_for('auth.signin'))
    return render_template('signin.html', siform=siform)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    rform = RegisterForm()
    if request.method == 'POST': # user submitted form
        if rform.validate_on_submit():
            # ok, the user gave us proper form input
            # actually go about signing the user in (more on this tomorrow)
            newuser = User(rform.username.data, rform.email.data, rform.password.data, rform.first_name.data, rform.last_name.data)
            try: # will produce an error if the username or password is taken
                db.session.add(newuser)
                db.session.commit()
            except:
                flash(f'That username or email is taken. Please try a different one.', category='danger')
                return redirect(url_for('auth.register'))
            login_user(newuser)
            # successful registration - redirect user to homepage
            flash(f'Successfully registered! Welcome, {rform.first_name.data}!', category='success')
            return redirect(url_for('home'))
        else:
            # bad form info - tell them to try again
            flash('Your passwords did not match or you provided an improper email/username. Try again.', category='danger')
            return redirect(url_for('auth.register'))
    return render_template('register.html', rform=rform)


@auth.route('/logout')
@login_required
def signout():
    logout_user()
    flash('You have been signed out.', category='info')
    return redirect(url_for('auth.signin'))