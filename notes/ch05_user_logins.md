ch05_user_logins.md

## User Logins

### Password Hashing

We store a hash of the user's supplied password using provided crypto libraries. Never store plaintext passwords.

Add `set_password()` and `check_password()` methods to the `User` model in `app/models.py`

```python
from werkzeug.security import generate_password_hash, check_password_hash

# ...

class User(db.Model):
    # ...

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

Open a `flask shell` session and enter the following to see how this works:

```python
>>> u = User(username='susan', email='susan@example.com')
>>> u.set_password('mypassword')
>>> u.check_password('password')
False
>>> u.check_password('mypassword')
True
```

### Intro to Flask-Login

The Flask-Login extension manages the user logged-in state, allowing for a user to remain logged in as they navigate from page to page.

`(venv) $ pip install flask-login`

Initialize this extension in `app/__init__.py`:

### Prepare User Model for Flask-Login

Flask-Login requires the following four items:

* `is_authenticated`: **True** if user has valid credentials; **False** otherwise
* `is_active`: **True** if user's account is active; **False** otherwise
* `is_anonymous`: **False** for regular users; **True** for sepcial, anonymous users
* `get_id()`: method that returns unique id for the user as a string

Flask-Login provides a _mixin_ class called **UserMixin** that includes generic implementations that are appropriate for most user model classes.

Add the mixin to the model:

```python
# ...
from flask_login import UserMixin

class User(UserMixin, db.Model):
    # ...
```

### User Loader Function

Flask-Login stores a unique identifier in Flask's user session: space assigned to each user connecting to the application.

With each page request from a user, Flask-Login retrieves the ID of the user from the session and loads that user into memory (db operation).

Flask-Login needs app's help in loading users. It needs to be able to call the function to load a user given the ID. Place this in the `app/models.py` module:

```python
from app import login
# ...

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
```

The user loader is registered with a decorator and will be called by login when a user needs to be [re]loaded.

### Logging Users In

We need to fix the login function to actually:

* access users from the database
* check their passwords
* maintain their "logged in" state, if desired

```python
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
        # Finally, redirect logged in user to the index page
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
```

### Logging Users Out

Modify `app/routes.py` to import the logout_user() function. Add a route `/logout` that executes the `logout_user()` function and redirects the user to the `/index` page.

```python
# ...
from flask_login import logout_user
# ...

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
```

Add conditional login and logout links to `app/templates/base.html`

### Requiring Users to Log In

Simply using a decorator (`@login_required`) with a view function, a user's credentials can be required to access that particular view.

`app/__init__.py`
```python
# ...
login = LoginManager(app)
login.login_view = 'login'
```

Then add decorators above view functions in `app/routes.py`:
```python
from flask_login import login_required

@app.route('/')
@app.route('/index')
@login_required
def index():
    # ...
```

But we want to include the user's original destination in the query string, so that we can redirect them to that location after they successfully authenticate.

Stopping at page 58 in book.
 Done
  Upated overall notes with 'next' support
  Added 'next' support to `routes.py`
 Todo
  Add 'next' notes to ch05 notes (this page)
  Test user login with shell-added user