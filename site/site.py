from flask import Flask, render_template, request
#from app import app


app = Flask(__name__)


@app.route('/')
def index():
    #user = {'username': 'Miguel'}
    tops = \
    [
        {
            "title": "TITLE",
            "time": "9 mins",
        },
        {
            "title": "Check no time",
        },
        {
            "title": "Check no time",
        },
        {
            "title": "Check no time",
        },
        {
            "title": "Check no time",
        },
    ]
    return render_template('index.html', title='Home', tops=tops,)


@app.route('/login', methods=["GET", "POST"])
def login():
    print(request.method)
    if request.method == 'GET':
        email = request.args.get('email')
        pswd = request.args.get('password')
        return render_template('login.html')
    else:
        email = request.form['email']
        pswd = request.form['password']
        return index()


@app.route('/sing-up')
def singup():
    return render_template('singup.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
