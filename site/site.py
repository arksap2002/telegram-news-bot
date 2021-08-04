from flask import Flask, render_template
#from app import app


app = Flask(__name__)


@app.route('/')
@app.route('/index')
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
    ]
    return render_template('index.html', title='Home', tops=tops,)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
