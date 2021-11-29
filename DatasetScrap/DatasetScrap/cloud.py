from datetime import datetime, timedelta


def save_in_databases(item, databases):
    city = item["name"]
    days = []
    hours = []
    for day in item["historical"]:
        daily = __input_daily(city, item["historical"][day])
        days.append(daily)
        date = item["historical"][day]["date"]
        for hour in item["historical"][day]["hourly"]:
            hourly = __input_hourly(city, date, hour)
            hours.append(hourly)
    for database in databases:
        database.daily_collection.insert_many(days)
        database.hourly_collection.insert_many(hours)
    print("days: ", len(days))
    print("hours", len(hours))


def find_highest_temp_in_hour(database, hour):
    x = database.hourly_collection.find_one({"time": hour}, {'_id': 0, 'temperature': 1}, sort=[("temperature", -1)])
    return x["temperature"]


def get_day_count(database):
    return database.daily_collection.find({}).count()


def get_hour_count(database):
    return database.hourly_collection.find({}).count()


def get_lowest_temperature_in_hour_group_by_city(database, hour):
    x = database.hourly_collection.aggregate([{
        "$match": {"time": hour}}, {
        "$group": {"_id": {"city": "$city"},
                   "avgTemp": {"$avg": "$temperature"}}}])
    print(list(x))
    return x


def __input_daily(city, item):
    date = datetime.strptime(item["date"], "%Y-%m-%d")
    day = dict()
    day["city"] = city
    day["date"] = date
    day["year"] = date.year
    day["month"] = date.month
    day["day"] = date.day
    day["mintemp"] = item["mintemp"]
    day["maxtemp"] = item["maxtemp"]
    day["avgtemp"] = item["avgtemp"]
    day["totalsnow"] = item["totalsnow"]
    day["sunhour"] = item["sunhour"]
    day["uv_index"] = item["uv_index"]
    return day


def __input_hourly(city, date_string, item):
    hour = item.copy()
    time = int(hour["time"]) // 100
    date = datetime.strptime(date_string, "%Y-%m-%d") + timedelta(hours=time)
    hour["city"] = city
    hour["date"] = date
    hour["year"] = date.year
    hour["month"] = date.month
    hour["day"] = date.day
    hour["time"] = time
    return hour
