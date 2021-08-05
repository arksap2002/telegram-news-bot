import sys, os

sys.path.insert(1, os.getcwd() + '/../')
print(sys.path)

from flask import (
    Flask, 
    render_template, 
    request,
    session,
)

from flask_login import (
    login_user, 
    logout_user, 
    current_user, 
    login_required
)

from loading import *


app = Flask(__name__)


@app.route('/')
def index():
    print(type(session))
    tops = \
    [
        {
            'title': 'TITLE',
            'time': '9 mins',
        },
        {
            'title': 'Check no time',
        },
        {
            'title': 'Check no time',
        },
        {
            'title': 'Check no time',
        },
        {
            'title': 'Check no time',
        },
    ]
    return render_template('index.html', title='Home', tops=tops, debug=app.debug)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        email = request.args.get('email')
        pswd = request.args.get('password')
        return render_template('login.html')


    email = request.form['email']
    pswd = request.form['password']



    return index()


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/sing-up')
def singup():
    return render_template('singup.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
