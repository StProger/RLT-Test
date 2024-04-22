from pymongo import MongoClient


def get_database():
    """ Connect to MongoDB server and return database """

    client = MongoClient()

    return client["pymongo_test"]
