from common.database import Database
from models.user import User

__author__ = 'Rory'

from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "urmumhavetriplegay"


@app.route('/')
def home_page():
    render_template('home.html')


# function called if link is accessed at specified endpoint
@app.route('/login')  # www.mysite.com/api/
def default_login_page():
    return render_template('login.html')


@app.route('/register')  # www.mysite.com/api/
def default_register_page():
    return render_template('register.html')

@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email=email, password=password):
        User.login(email)
    else:
        session['email'] = None

    return render_template('profile.html', email=session['email'])


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)

    return render_template('profile.html', email=session['email'])


if __name__ == '__main__':
    app.run(port=3)
