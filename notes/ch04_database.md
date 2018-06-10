ch04_database.md

## Database

### Databases in Flask

* No native support for databases in Flask, by design.
* Two big types of of databases: relational and non-relational ("NoSQL")

Installing a few more Flask extensions:

* Flask-SQLAlchemy is an ORM to multiple databases: MySQL, PostgreSQL, SQLite
`(venv) $ pip install flask-sqlalchemy`

### Database Migrations

Migrations are necessary becuase data needs to be migrated to a new database schema, particularly in the case of non-additive schema operations.

Install Flask-Migrate, a wrapper for Alembic:

`(venv) $ pip install flask-migrate`

### Flask-SQLAlchemy Configuration

We'll use a SQLite database for development. These are file-based and don't require a database server.

Add the SQLite database information to `config.py`:

```python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

We can either use an environment variable to provide the location of the database or fallback to a default value of `sqlite:///<location of app>/app.db`

We also need to add import statements and create instances in `app/__init__.py` of :
* SQLAlchemy
* Migrate

We'll also import the `models` module to define the structure of the database.

### Database Models

Create a model that represents users, including:
* id INTEGER
* username VARCHAR (64)
* email VARCHAR (120)
* password hash VARCHAR (128)

An `id` field is usually present in all models and typically used as the _primary key_. This value is typically auto-assigned (auto-incremented) by the database on the creation of a new row.

Create the `app/models.py` module to begin building out models that will translate (automatically, via SQLAlchemy) into database schema representations.

```python
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)
```

We create a `User` class from the `db.Model`, a base class for all models from Flask-SQLAlchemy.

Fields are created as instances of the `db.Column` class, with the first argument _field type_, along with other optional arguments.

We create a field for each column we'd like to see in the `User` table and specify constraints such as _primary key_, _uniqueness_, etc.

Finally, we add a method (`__repr__(self)`) that allows us to print objects of this (`User()`) class in a Python interpreter session.

### Creating Migration Repository

Ensure that the `FLASK_APP` environment variable is set (in this case, to `microblog.py`)

`(venv) $ flask db init` will create the first instance of the database

- This will create a new migrations directory with instructions necessary for Alembic to migrate the database schema via SQL commands
- This migrations directory MUST be tracked in source control – it contains all of the successive instructions to assemble the database to a particular state

### The First Database Migration

`(venv) $ flask db migrate -m "<migration message>"`

- This will generate the first migration, which is a set of instructions to generate the users table that will map to the `User` database model.
- Alembic can create this migration automatically, and will automatically populate the migration script with changes needed to the database schema to match the application models.
- Because there is no previous database in this case, the automatic migratino will add the entire User model to the migration script.
- Subsequent migrations may just be adding or removing a column, thereby only modifying the schema.
- The generated script is now part of the project and must remain with source control.
- The generated script has two functions: `upgrade()` and `downgrade()`
- `upgrade()` will apply the migration
- `downgrade()` will remove the migration

`(venv) $ flask db upgrade`

- This applies the migration script
- SQLite database is not found and is therefore created

### Database Upgrade and Downgrade Workflow

