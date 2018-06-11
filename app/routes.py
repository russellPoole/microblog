from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required

# Need to import User model because user concept  is so important when it comes to authentication
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Dwight'}
    posts = [
        {
            'author': {'username': 'Michael'},
            'body': 'Beautiful day in New York!'
        },
        {
            'author': {'username': 'Angela'},
            'body': 'Enjoying Westworld.'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, don't show /login screen
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Load user from database
        user = User.query.filter_by(username=form.username.data).first()
        # If user is not found, OR their supplied password doesn't validate,
        # redirect them to the /login screen and flash the error message
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # if user successfully loads, execute the login_user function,
        # along with the boolean for remembering them beyond their browser
        # session
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        # Finally, redirect logged in user to the index page
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))