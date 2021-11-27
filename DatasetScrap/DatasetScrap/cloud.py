import requests as requests
from pymongo import MongoClient
from DatasetScrap.DatasetScrap.spiders.dataset_spider import DatasetSpider
from DatasetScrap.DatasetScrap.items import DatasetscrapItem

from scrapy.selector import Selector

def parse(response):
    print("pres runs")
    n=0
    client = MongoClient("mongodb+srv://togrzesik:<password>@cluster0.vyuku.mongodb.net/test")
    db = client.get_default_database('weather')
    records = db.data

    rows = Selector(response).xpath("//table[@class='mat-table cdk-table mat-sort ng-star-inserted']//tbody//tr")
    for row in rows:
        print('int(n) is:', int(n))
        new_item = {
            'time': row.xpath('td[1]//text()').extract_first(),
            'temperature': row.xpath('td[2]//text()').extract_first(),
            'humidity': row.xpath('td[4]//text()').extract_first(),
            'wind_speed': row.xpath('td[6]//text()').extract_first(),
        }

class cloud:
    client = MongoClient()
    db = client.get_default_database('weather')
    records = db.data

    def input_item(records):
        new_item = {
            'date': 'na',
            'roll_no': 321,
            'name2': 'me'
        }
        records.insert_one(new_item)
        return new_item

    req = requests.get('https://www.wunderground.com/history/daily/pl/balice/EPKK/date/2017-11-27?fbclid=IwAR0nU8r8TW4-66lOT7zhdySOiAoPdtK-_aCj_cYZE_QS9Cf4E9CP0jhVLDU')
    parse(req)