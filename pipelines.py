# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class Book24Pipeline:
    def __init__(self):
        client = MongoClient('localhost:27017')
        self.mongo_db = client.Books24_DB

    def process_item(self, item, spider):
        books_collection = self.mongo_db[spider.name]
        books_collection.insert_one(item)
        return item
