import requests
import json

class WeatherstackWebClient:
    def __init__(self):
        self.__address = "https://api.weatherstack.com/historical?access_key=750bee067c998111c49f4b6257731381&hourly=1&interval=1&query="
        self.__keys_to_take = ["time", "temperature", "wind_speed", "wind_degree", "wind_dir", "humidity", "pressure",
                            "feelslike", "uv_index", "chanceofrain", "chanceofsnow", "chanceofthunder"]

    def get_historical_data(self, city, year, month):
        days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        length = days[month]
        if month + 1 == 2 and year % 4 == 0:
            length += 1
        url = self.__build_url(city, year, month, length)
        print(url)
        data = requests.get(url=url)
        json_data = data.json()
        print("Data:\n", json_data, "\n")
        return self.__parse(json_data)

    def __parse(self, response):
        city = dict()
        city["name"] = response["location"]["name"]
        city["location"] = response["location"]
        city["historical"] = dict()
        for date in response["historical"]:
            city["historical"][date] = response["historical"][date].copy()
            city["historical"][date]["hourly"] = []

            for hour in response["historical"][date]["hourly"]:
                info = dict()
                for k in self.__keys_to_take:
                    info[k] = hour[k]
                city["historical"][date]["hourly"].append(info)
        return city

    def __build_url(self, city, year, month, length):
        url = self.__address + city
        url += self.__create_query_date_string("start", year, month, 1)
        url += self.__create_query_date_string("end", year, month, length)
        return url

    def __two_digit_string(self, number):
        if number >= 10:
            return str(number)
        return "0" + str(number)

    def __create_query_date_string(self, name, year, month, day):
        day_string = self.__two_digit_string(day)
        month_string = self.__two_digit_string(month + 1)
        return "&historical_date_" + name + "=" + str(year) + "-" + month_string + "-" + day_string