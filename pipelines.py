# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient


class GrustnogramApiParsingPipeline:
    def __init__(self):
        client = MongoClient('localhost:27017')
        self.mongo_db = client.Grustnogram_DB

    def process_item(self, item, spider):
        grustnogram_user_follows = self.mongo_db[spider.parse_user]
        grustnogram_user_follows.insert_one(item)
        return item
