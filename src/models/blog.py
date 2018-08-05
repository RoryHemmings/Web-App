import uuid

from common.database import Database
from models.post import Post


class Blog:
    def __init__(self, author, title, description, author_id, _id=None):
        self.title = title
        self.author = author
        self.description = description
        self.author_id = author_id
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self, title, content):  # create new post with this as parent id, title of post content and author
        post = Post(self._id, title, content, self.author)
        post.save_to_mongo()

    def get_posts(self):  # returns list of posts under this parent blog
        return Post.from_blog(self._id)

    def save_to_mongo(self):  # inserts json with blog data into the database
        Database.insert('blogs', self.json())

    def json(self):  # returns dictionary with data about blog
        return {
            'author': self.author,
            'title': self.title,
            'description': self.description,
            'author_id': self.author_id,
            '_id': self._id
        }

    @classmethod
    def get_from_mongo(cls, id):  # returns Blog object with corresponding id
        # blog_data: compass object, json children are accessed by dictionary
        blog_data = Database.find_one(collection='blogs', query={'_id': id})
        return cls(**blog_data)

    @classmethod
    def find_by_author_id(cls, author_id):  # returns list of Blog objects with specified author ids
        blogs = Database.find(collection="blogs", query={'author_id': author_id})
        return [cls(**blog) for blog in blogs]

