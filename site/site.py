from flask import (
    Flask, 
    render_template, 
    request,
    session,
    flash,
)

from flask_login import (
    login_user, 
    logout_user, 
    current_user, 
    login_required,
    login_manager,
    LoginManager,
)

from data_processing.loading import *


app = Flask(__name__)
app.secret_key = 'some key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def user_loade(user_id):
    print(user_id)
    if user_id in cur_users.keys():
        print(current_user.is_authenticated)
        return cur_users[user_id]
    else:
        print(None)
        return None


@app.route('/')
def index():
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

    add_to_current_or_create_user(email, email, pswd)
    user = cur_users[email]

    if login_user(user, remember=True):
        print("Logged in!")
    else:
        print("unable to log you in")
    return index()


@app.route('/is-logged')
def test_loggedin():
    return render_template('test_loggedin.html', user=current_user if current_user.is_authenticated else None)

#@app.route('/test')
#def test():
#    return render_template('test.html', user=current_user if current_user.is_authenticated else None)


@app.route('/sing-up')
def singup():
    return render_template('singup.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
