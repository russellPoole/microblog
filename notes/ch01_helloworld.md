# Chapter 1: Hello, World!

## Verify python3 installed locally

`$python 3 --version`

## Create GitHub Repository

Ensure SSH keys are created locally (and in SSH config) and the public key is copied to GitHub.

To test this connection, execute the following in a terminal session: `ssh -T git@github.com`

Sign in to GitHub and create a new repository that will serve as the remote origin for your project.

Be sure to include the .gitignore file for Python.

When the repository is created on GitHub, navigate via a terminal sesison to the local directory in which the remote repository will be created as the local working directory. Execute the following command, replacing the variables appropriately:

`git clone git@github.com:<github_username>/<repo_name>.git`

Navigate into the new directory on your local machine. You are now in the working directory.

## Create and Activate Virtual Environment

`$ python3 -m venv venv`

`$ source venv/bin/activate`

Your Python executable is now located in the `venv` directory created in this step. This is also where all packages for the Python applicaiton will be located.

## Install Flask

`(venv) $ pip install flask`

## Create a "Hello, World" Flask App

`(vnev) $ mkdir app`

Navigate into the directory and add the code for `app/__init__.py`

You also need to create `app/routes.py`, which is referenced by `__init__.py`

Finally, in the top level (up one), create `microblog.py`, which will define the Flask application instance.

The directory should appear as follows:
`microblog/`
`   venv/`
`   app/`
`     __init__.py`
`     routes.py`
`   microblog.py`

## Export Environment Variable

`(venv) $ export FLASK_APP=microblog.py`

## Run the Application!

`(venv) flask run`

Navigate to `http://127.0.0.1:5000/`, `http://127.0.0.1:5000/index`, or `http://localhost:5000/` in your browser to see the Flask application running locally.

Pres `Ctrl + C` to stop the web server.