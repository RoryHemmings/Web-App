import uuid

from flask import session

from common.database import Database
from models.blog import Blog


class User:
    def __init__(self, email, password, nickname, _id=None):  # create User object with specified email, password and id is
        self.email = email                          # randomly generated
        self.password = password
        self.nickname = nickname
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_user_by_email(cls, email):  # returns User object width specified email, if user is found
        user_data = Database.find_one("users", {'email': email})
        if user_data is not None:
            return cls(**user_data)

    @classmethod
    def get_user_by_id(cls, id):  # returns User object width specified id, if user is found
        user_data = Database.find_one("users", {'_id': id})
        if user_data is not None:
            return cls(**user_data)

    @staticmethod
    def login_valid(email, password):  # check if specified password is valid
        # User.login_valid('rpmhemmings@gmail.com', '12345')
        user = User.get_user_by_email(email)
        if user is not None:
            # check if user from database's password is the same as the password passed in
            return user.password == password
        return False

    @classmethod
    def register(cls, email, password, nickname):  # if user does not already exist, User object is created and saved to database
        user = cls.get_user_by_email(email)  # with specified credentials
        if user is None:
            new_user = cls(email, password, nickname)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            # user does exist
            return False

    @staticmethod
    def login(user_email):  # sets users session to their email
        # Login has been called
        session['email'] = user_email

    @staticmethod
    def logout():  # resets users session
        session['email'] = None

    def get_blogs(self):  # returns list of Blog objects with this authors author_id
        return Blog.find_by_author_id(self._id)

    def new_blog(self, title, description):  # creates a new blog with this users email and id and specified id, saves
        blog = Blog(author=self.email, title=title, description=description, author_id=self._id)
        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content):  # creates new post with specified blog id and title, content...
        blog = Blog.get_from_mongo(blog_id)
        blog.new_post(title, content)

    def json(self):  # returns this objects data in json form
        return {
            'email': self.email,
            '_id': self._id,
            'password': self.password,
            'nickname': self.nickname
        }

    def save_to_mongo(self):  # inserts this objects json data into the database
        Database.insert('users', self.json())
