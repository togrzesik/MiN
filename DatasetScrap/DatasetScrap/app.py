from DatasetScrap.DatasetScrap.cloud import Mongo
from DatasetScrap.DatasetScrap.weatherstackWebClient import WeatherstackWebClient


load_data = False


class App:
    def __init__(self):
        self.__cities = ["Warsaw", "London", "Berlin", "Madrid", "Rome", "Paris", "Moscow"]
        year_start = 2015
        year_end = 2020
        self.__years = range(year_start, year_end + 1)
        self.__cloud_database = Mongo(
            "mongodb+srv://min_admin:admin_min@cluster0.aqbvi.mongodb.net/weather?retryWrites=true&w=majority")
        self.__local_database = Mongo("mongodb://localhost:27017")
        self.__web_client = WeatherstackWebClient()

    def get_and_save_historical_data(self):
        databases = [self.__cloud_database, self.__local_database]
        for city in self.__cities:
            for year in self.__years:
                for month in range(12):
                    data = self.__web_client.get_historical_data(city, year, month)
                    for database in databases:
                        database.input_item(data)


if __name__ == "__main__":
    app = App()
    if load_data:
        print("loading data\n")
        app.get_and_save_historical_data()
