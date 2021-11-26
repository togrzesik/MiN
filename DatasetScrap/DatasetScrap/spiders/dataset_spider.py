from scrapy import Spider
from scrapy.selector import Selector
from DatasetScrap.DatasetScrap.items import DatasetscrapItem
#from DatasetScrap.items import DatasetscrapItem

class DatasetSpider(Spider):
    name = "dataset"
    allowed_domains = ["github.com"]
    start_urls = [
    ]

    def parse(self, response):