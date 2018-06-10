ch02_templates.md

Add the raw HTML to be rendered into the index() function in `app/routes.py`. The raw HTML string will contain a Python variable representing the a mock user that will be rendered into the string before display in the browser.

Obviously this is tedious and not scalable. We will undo this and move the view / presentation layer into templates.

Create a new directory `templates`: `(venv) $ mkdir app/templates`

Create a new file `app/templates/index.html` and add the HTML template code.

Add the `render_template()` function to `app/routes.py`

The `render_template()` function will need to be imported, and will be passed variables necessary to populate the template variables `{{ title }}` and `{{ user }}`. The first argument to the function is the filename of the template to be rendered.

## Conditional Statements

The Jinja template language allows for conditionals to be evaluated at the time of template rendering, using the arguments passed to the rendering function.

<br>`{% if <test> %}`
<br>`<p>code block 1</p>`
<br>`{% else %}`
<br>`<p>code block 2</p>`
<br>`{% endif %}`

## Loops

Lists can be passed as arguments to the template rendering function, which can be evaluated sequentially at the time of rendering.

<br>`{% for item in items %}`
<br>`<p> {{ item.attribute1 }} {{ item.attribute2 }}</p>`
<br>`{% endofr %}`

## Template Inheritance

Much of the HTML code will be repeated from page to page. For example, the header, navbar, footer, etc., will largely be the same between page loads, perhaps varying on some conditionals. Because of this, we don't need to rewrite all of the HTML to be rendered for each page. The other benefit of template inheritance is that changes made to an inherited piece of code will be propagated across the entire application, without the need to update multiple template files.

The base template needs to include the following block where downstream content will be inserted `app/templates/base.html`:

`{% block content %}{% endblock %}`

The template to inherit from the base template (`app/templates/index.html`) will need to include the following:

<br>`{% extends "base.html" %}`
<br>
<br>`{% block content %}`
<br>`...content to be inserted...`
<br>`{% endblock %}`

## Git Operations

Save, add, commit, push.