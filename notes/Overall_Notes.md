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

### Form Addition Order

1. `app/forms.py`: Import necessary form field types, imporrt necessary validators, create new form class with each form field as a class variable. 
2. `app/templates<form_page>.html`: Create / modify form template to interact with newly-created Form class in step 1. This template will receive the above Form class as a variable during rendering.
3. `app/routes.py`: Import the new Form class form `app.forms`. Add / modify a view function that will render the template referenced in step 2. Upon successful submission, you will likely want to redirect to a different route bu returning `redirect(url_for('<view_function>'))`

### Route Pattern to Display Forms

`from flask import render_template, flash, redirect, url_for`
<br>`from app.forms import FormClassName`
<br>`...`
<br>`@app.route('/<route>', methods=['GET', 'POST'])`
<br>`def <view_function>():`
<br>&nbsp;&nbsp;&nbsp;&nbsp;`form = <FormClassName>()`
<br>&nbsp;&nbsp;&nbsp;&nbsp;`if form.validate_on_submit():`
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`flash('<message to flash>')`
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return redirect(url_for('<target_view_function>')`
<br>&nbsp;&nbsp;&nbsp;&nbsp;`return render_template('<form_template>.html', title='<form page title>', form=form)`

