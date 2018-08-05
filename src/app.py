from common.database import Database
from models.user import User

__author__ = 'Rory'

from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "urmumhavetriplegay"


# function called if link is accessed at specified endpoint
@app.route('/')  # www.mysite.com/api/
def default_page():
    return render_template('login.html')

@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email=email, password=password):
        User.login(email)
    else:
        session['email'] = None

    return render_template('profile.html', email=session['email'])


if __name__ == '__main__':
    app.run(port=3)
