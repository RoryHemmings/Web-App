import pymongo


class Database:
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():  # creates variable to access database
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection, data):  # inserts data into database at specified collection, collection is like category
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):  # returns compass list object with results from query in specified collection
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):  # returns compass object with results from query in specified collection
        return Database.DATABASE[collection].find_one(query)