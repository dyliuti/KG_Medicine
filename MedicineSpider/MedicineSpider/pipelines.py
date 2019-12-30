# -*- coding: utf-8 -*-
# Authon: yanminwei
# Date: 2019/11/18

import pymongo
from scrapy.exceptions import DropItem

class MedicinespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item['basic_info'].get('name', None) is None:
            return DropItem
        collection_name = 'test'
        self.db[collection_name].insert(dict(item))
        return item