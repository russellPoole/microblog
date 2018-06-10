from app import app

@app.route('/')
@app.route('/index')
def index():
    return '你好, World!'