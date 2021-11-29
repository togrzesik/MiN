from pymongo import MongoClient


class Mongo:
    def __init__(self, address):
        client = MongoClient(address)
        db = client.minadzd_project
        self.daily_collection = db.daily
        self.hourly_collection = db.hourly
