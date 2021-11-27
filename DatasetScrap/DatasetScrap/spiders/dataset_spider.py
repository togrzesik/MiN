from scrapy import Spider
from scrapy.selector import Selector
from DatasetScrap.DatasetScrap.items import DatasetscrapItem
#from DatasetScrap.items import DatasetscrapItem

class DatasetSpider(Spider):
    name = "dataset"
    allowed_domains = ["wunderground.com"]
    start_urls = [
        "https://www.wunderground.com/history/daily/pl/balice/EPKK/date/2017-11-27?fbclid=IwAR0nU8r8TW4-66lOT7zhdySOiAoPdtK-_aCj_cYZE_QS9Cf4E9CP0jhVLDU"
    ]

    def parse(self, response):
        rows = Selector(response).xpath("//table[@class='mat-table cdk-table mat-sort ng-star-inserted']//tbody//tr")
        for row in rows:
            item = DatasetscrapItem()
            item['time'] = row.xpath('td[1]//text()').extract_first()
            item['temperature'] = row.xpath('td[2]//text()').extract_first()
            item['humidity'] = row.xpath('td[4]//text()').extract_first()
            item['wind_speed'] = row.xpath('td[6]//text()').extract_first()
            yield item