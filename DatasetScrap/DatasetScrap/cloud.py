from pymongo import MongoClient


class Mongo:
    def __init__(self, address):
        client = MongoClient(address)
        db = client.minadzd
        self.__records = db.weather

    def input_item(self, item):
        name = item["name"]
        if self.exists(name):
            city = self.find_by_city_name(name)
            for date in item["historical"]:
                city["historical"][date] = item["historical"][date]
            return self.update_historical_by_city_name(name, city["historical"])
        self.__records.insert_one(item)
        return item

    def find_by_city_name(self, city):
        return self.__records.find_one({"name": city})

    def update_historical_by_city_name(self, city_name, historical):
        query = {"name": city_name}
        new_values = {"$set": {"historical": historical}}
        self.__records.update_one(query, new_values)
        return self.find_by_city_name(city_name)

    def exists(self, city_name):
        return self.__records.count_documents({'name': city_name}, limit=1) != 0

    def collection(self):
        return self.__records
