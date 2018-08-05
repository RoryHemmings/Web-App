__author__ = 'Rory'

from flask import Flask, render_template

app = Flask(__name__)


# function called if link is accessed at specified endpoint
@app.route('/')  # www.mysite.com/api/
def default_page_method():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(port=3)
