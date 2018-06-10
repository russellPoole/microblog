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

### Adding New Models

TODO

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