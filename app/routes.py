from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
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