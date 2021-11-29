from datetime import datetime

from DatasetScrap.DatasetScrap.cloud import save_in_databases, find_highest_temp_in_hour, get_day_count, get_hour_count,\
    get_lowest_temperature_in_hour_group_by_city, get_max_temp_group_by_city_and_month
from DatasetScrap.DatasetScrap.mongo import Mongo
from DatasetScrap.DatasetScrap.weatherstackWebClient import WeatherstackWebClient


load_data = False


class App:
    def __init__(self):
        self.__cities = ["Warsaw", "London", "Berlin", "Madrid", "Rome", "Paris", "Moscow"]
        year_start = 2015
        year_end = 2020
        self.__years = range(year_start, year_end+1)
        self.__cloud_database = Mongo(
            "mongodb+srv://min_admin:admin_min@cluster0.aqbvi.mongodb.net/weather?retryWrites=true&w=majority")
        self.__local_database = Mongo("mongodb://localhost:27017")
        self.__web_client = WeatherstackWebClient()
        self.__databases_list = [self.__cloud_database, self.__local_database]
        self.__databases = {"Cloud": self.__cloud_database, "Local": self.__local_database}

    def get_and_save_historical_data(self):
        for city in self.__cities:
            for year in self.__years:
                for month in range(12):
                    data = self.__web_client.get_historical_data(city, year, month)
                    save_in_databases(data, self.__databases_list)

    def find_highest_temp_in_hour(self, hour):
        self.__execute_with_param(find_highest_temp_in_hour, hour)

    def day_count(self):
        self.__execute(get_day_count)

    def hour_count(self):
        self.__execute(get_hour_count)

    def lowest_temperature_in_hour_group_by_city(self, hour):
        self.__execute_with_param(get_lowest_temperature_in_hour_group_by_city, hour)

    def max_temp_group_by_city_and_month(self):
        self.__execute(get_max_temp_group_by_city_and_month)

    def __execute(self, fun):
        for database in self.__databases:
            start = datetime.now()
            result = fun(self.__databases[database])
            end = datetime.now()
            print("Database: ", database, " | Result: ", result, " | Time: ", end - start)

    def __execute_with_param(self, fun, param):
        for database in self.__databases:
            start = datetime.now()
            result = fun(self.__databases[database], param)
            end = datetime.now()
            print("Database: ", database, " | Result: ", result, " | Time: ", end - start)


if __name__ == "__main__":
    app = App()
    if load_data:
        print("loading data\n")
        app.get_and_save_historical_data()
    app.max_temp_group_by_city_and_month()
