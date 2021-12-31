# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.books

    def process_item(self, item, spider):
        authors, name = item['name'].split(': ')
        item['name'] = name
        for i in ['old_price', 'discount_price', 'rating']:
            try:
                item[i] = float(item[i])
            except Exception as e:
                pass
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item
