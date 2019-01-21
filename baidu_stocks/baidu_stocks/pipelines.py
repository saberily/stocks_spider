# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class BaiduStocksPipeline(object):  # 将数据存入TXT文件中
    def open_spider(self,spider):
        self.file = open('stock_id.txt','w',encoding='GBK')

    def close_spider(self,spider):
        self.file.close()
        print('ok')

    def process_item(self, item, spider):
        try:
            item = dict(item)
            if len(item) > 2:
                self.file.write(str(item)+'\n')
        except:
            pass
        return item




import pymongo

class MongoPipeline(object):  # 将数据入库


    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            item = dict(item)
            if len(item) > 2:
                self.db['stocks_info'].insert_one(dict(item))
        except:
           pass
        return item
