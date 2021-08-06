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
def user_loader(user_id):
    return cur_users[user_id] if user_id in all_users.keys() else None
    #return User.get(user_id)


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

    add_to_current_or_create_user(email)
    user = cur_users[email]

    if login_user(user, remember=True):
        print("Logged in!")
        #return redirect('/notes/create')
    else:
        print("unable to log you in")
    return index()


@app.route('/test')
def test():
    print(type(current_user))
    print(current_user)
    try:
        print(current_user.is_authenticated())
    except:
        print("func faill")
    try:
        print(current_user.is_authenticated)
    except:
        print("peremennaya faill")
    return render_template('test.html', user=current_user if current_user.is_authenticated else None)


@app.route('/sing-up')
def singup():
    return render_template('singup.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
