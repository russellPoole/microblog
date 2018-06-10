ch03_webforms.md

## Webforms
### Flask-WTF
Extension to make working with forms easier.

`(venv) $ pip install flask-wtf`

### Configuration

We want to move application configuration to a single location to make updates easier in the future. Instead of placing config variables in `__init__.py`, we'll import a separate config module from the top level directory.

Create `config.py` with a `Config` class in the top level (above `app`) directory. This will contain class variables that represent application configuration values. Some of these variables will be populated from environment variables, so as to prevent secret variables from being hardcoded.

Using a class has the added benefit of subclassing, perhaps for different environments (INT, STG, PRD).

In `__init__.py`, import `Config` from the `config` module, and use `app.config.from_object(Config)` to point to the imported configuration variables.

### User Login Form

We'll create a separate module – `app/forms.py` – to house all of our app's forms. Start by creating a user login form.

Each form to be used is an subclass of the FlaskForm class. For each field to be used in the form, an object is created as a class variable in the `LoginForm` class.

### Form Templates

After creating the form class, we need to create a template that will display, accept, and process variables to and from the web browser.

### Form Views

Finally, `routes.py` must be updated to:

* import the new `LoginForm` class
* provide a route to the new page to be rendered
* pass an instance of hte `LoginForm` class to the `render_template()` function

Navigating to the new route should render the form to receive input. Clicking the "Sign In" button returns an error at this point because the form's method is set to `POST`. The login route is currently only using a (default) `GET` method.

### Receiving Form Data

We need to add the set of methods to be supported on the `/login` route: `GET` and `POST`.

We'll also need to additional functions imported from the flask module: `flash` and `redirect`.

A method, `validate_on_submit()` is called when the form is submitted (`POST`ed) with a fully valid set of data. Using a conditional, if valid data is submitted to the form, we can invoke the `redirect()`  function to send the user to another route. If no data is sumbitted (user is loading the page instead of clicking "Sign In" on the page) or the data submitted does not completely validate, we will skip the if and return the original form template.

We are also using `flash()` as part of the _true_ path of the conditional. This allows for a simple message to be passed to the following page being rendered. We'll need to add the ability to display flashed messages to the template. We'll always want the ability to display flashed messages, so we should add this to the `app/templates/base.html` template.

### Improving Field Validation

We want to provide a user with feedback about their form entries that failed validation. We can display these as a list of errors beneath the form field by referencing the collected errors in the Form field object (`form.<formfield>.errors`) on prior submission. If no submission took place or there were no errors on that particular field, the list will be empty. Template looping can control the display of the error(s) as a list.

### Generating Links

Hardcoding of links should always be avoided because the routes referenced are subject to change at any point in the future.

View functions, by contrast, are likely to be more stable. By using the `{{ url_for('<target_view_function>' )}}` convention in place of links in templates, the target view function route can be looked up and rendered dynamically.

The `@app.route` listed last is the value that will be used when generating links.

Remember to import the `url_for()` function from `flask` in `routes.py`