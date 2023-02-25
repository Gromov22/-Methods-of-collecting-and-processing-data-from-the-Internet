# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class MvideoParsingPipeline:
    def __init__(self):
        client = MongoClient('localhost:27017')
        self.mongo_db = client.Cars_DB

    def process_item(self, item, spider):
        cars_collection = self.mongo_db[spider.name]
        cars_collection.insert_one(item)

        return item
