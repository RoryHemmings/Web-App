from common.database import Database
from models.blog import Blog
from models.post import Post
from models.user import User

__author__ = 'Rory'

from flask import Flask, render_template, request, session, make_response

app = Flask(__name__)
app.secret_key = "itsliterallyimpossibletobreakthissupersecurekey"


@app.route('/')
def home_page():
    return render_template('home.html')


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
    nickname = request.form['nickname']

    User.register(email, password, nickname)

    return render_template('profile.html', email=session['email'])


@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_user_by_id(user_id)
    else:
        user = User.get_user_by_email(session['email'])
    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogs, email=user.email, nickname=user.nickname)


@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_user_by_email(session['email'])

        new_blog = Blog(user.email, title, description, user._id)
        new_blog.save_to_mongo()

        return make_response(user_blogs(user._id))


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.get_from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template("posts.html", posts=posts, blog_title=blog.title, blog_id=blog._id,
                           nickname=User.get_user_by_id(Blog.get_from_mongo(blog_id).author_id).nickname)


@app.route('/posts/<string:blog_id>/new', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_post.html', blog_id=blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_user_by_email(session['email'])

        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))


if __name__ == '__main__':
    app.run(port=3)
