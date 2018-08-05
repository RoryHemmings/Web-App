# Post class v0.1
import uuid
import datetime

from common.database import Database


class Post:
    def __init__(self, blog_id, title, content, author, date=datetime.datetime.utcnow(), _id=None):
        # blog_id: id of parent blog
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.date = date
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):  # inserts json with corresponding post into the database
        Database.insert('posts', self.json())

    def json(self):  # returns dictionary with parent data
        return {
            '_id': self._id,
            'blog_id': self.blog_id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'date': self.date
        }

    @classmethod
    def get_from_mongo(cls, id):  # returns Post object with specified id
        post_data = Database.find_one('posts', {'_id': id})
        return cls(**post_data)

    @staticmethod
    def from_blog(id):  # return list with all posts in parent blog id
        posts = [post for post in Database.find(collection='posts', query={'blog_id': id})]
        return posts

    def __repr__(self):  # prints post data to console
        return "/n{title}/n{author}/n{date}/n/n{content}/n".format(title=self.title,
                                                                   author=self.author,
                                                                   date=self.date,
                                                                   content=self.content,
                                                                   id=self._id)
