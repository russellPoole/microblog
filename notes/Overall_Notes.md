Overall_Notes.md

### Run the application:

1. Set environment variable `FLASK_APP=microblog.py`
2. Execute `flask run`
3. Visit `http://localhost:5000/` in web browser

### Git Operations

1. `git status`
2. `git add *`
3. `git status`
4. `git commit -m "message"`
5. `git push origin master`
6. `git log --pretty=oneline` (note first ten characters of hash for latest commit)
7. `git tag v<value> <hashvalue>`
8. `git push origin --tags`

### Form Addition Order

1. **`app/forms.py`** Import necessary form field types, imporrt necessary validators, create new form class with each form field as a class variable. 
2. **`app/templates/<form_page>.html`** Create / modify form template to interact with newly-created Form class in step 1. This template will receive the above Form class as a variable during rendering.
3. **`app/routes.py`** Import the new Form class form `app.forms`. Add / modify a view function that will render the template referenced in step 2. Upon successful submission, you will likely want to redirect to a different route bu returning `redirect(url_for('<view_function>'))`

### Route Pattern to Display Forms

```python
from flask import render_template, flash, redirect, url_for
from app.forms import <FormClassName>
...
@app.route('/<route>', methods=['GET', 'POST'])
def <view_function>():
    form = <FormClassName>()
    if form.validate_on_submit():
        flash('<message to flash>')
        return redirect(url_for('<target_view_function>')
    return render_template('<form_template>.html', title='<form page title>', form=form)
```

### User Login Pattern

**`__init__.py`**
```python
from flask_login import LoginManager
# ...
app = Flask(__name__)
# ...
login = LoginManager(app)
# Let Flask-Login know whch view function handles logins (to be refernced by @login_required decorator)
login.login_view = 'login'
```

**`app/models.py`**
```python
from app import login
from flask_login import UserMixin
...
class User(UserMixin, db.Model):
# ...
```

**`app/routes.py`**
```python
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

# ...

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
```

### Adding New Models

* Add model to `app/models.py`
* Import model into `microblog.py` from `app.models`
* When ready, perform database migrations to reflect model in the database

### Model Pattern

```python
class <OneModelName>(db.Model):
    column_name_1 = db.Column(db.<ColumnType>, [options])
    ...
    one_many_relationship_column = db.relationship('ManyModelName', backref='<reference name as variable from other model>')

    def __repr__(self):
        return 'text representation {}'.format(self.column_name_n)

class <ManyModelName>(db.Model):
    column_name_1 = db.Column(db.<ColumnType>, [options])
    parent_relationship_column = db.Column(db.<ColumnType>, db.ForeignKey('onemodelname.column_name_1'))

    def __repr__(self):
        return 'text representation {}'.format(self.column_name_n)
```

ColumnTypes

* `db.Integer`
* `db.String(<length>)`
* `db.DateTime`

Column Options (not applicable to all column types)

* `primary_key=[]`
* `index=[]`
* `unique=[]`
* `default=[datetime.utcnow]`
* `db.ForeignKey('<table_name>.<column_name>')`


### Database Migration

Ensure that the `FLASK_APP` environment variable is set (in this case, to `microblog.py`)

1. `(venv) $ flask db init` will create the first instance of the database
    - This will create a new migrations directory with instructions necessary for Alembic to migrate the database schema via SQL commands
    - This migrations directory MUST be tracked in source control – it contains all of the successive instructions to assemble the database to a particular state
2. `(venv) $ flask db migrate -m "<migration message>"`
3. `(venv) $ flask db upgrade`
    - `(venv) $ flask db downgrade` can be used to remove the migration


### Querying the Database via Models

```python
>>> all_elements_of_a_class = <ModelName>.query.all()
>>> element_of_id_<n>_of_a_class = <ModelName>.query.get(<n>)
```

If an instance of a model is to be referenced as a foreign key in another model, it can be expressed as so:

```python
>>> foreign_key_element = OneModel.query.get(<n>)
>>> many_model_element = ManyModel(variable='value', foreign_key=foreign_key_element)
>>> db.session.add(many_model_element)
>>> db.session.commit()
```

### Shell Context

To make objects such as models and the database available in the shell context, we need to register these items in the root [`microblog.py`] application:

```python
from app import app, db
from app.models import Model1, Model2

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Model1': Model1, 'Model2': Model2}
```

```python
(venv) $ flask shell
>>> db
<SQLAlchemy engine=sqlite:////Users/<username>/dev/microblog/app.db>
>>> Model1
<class 'app.models.Model1'>
>>> Model2
<class 'app.models.Model2'>
```

### Extensions

`(venv) $ pip install <extension name>`

In `app/__init__.py`, initialize the newly-installed extension:

```python
from <flask_extension> import <ExtensionName>

app = Flask(__name__)
# ...
<extension> = ExtensionName(app)

# ...