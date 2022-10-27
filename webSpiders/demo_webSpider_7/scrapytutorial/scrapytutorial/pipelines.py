# Define your item pipelines here
# 当Item生成后，会自动被送到Item Pipeline进行处理
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pymongo


class TextPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        """
        启用Item Pipeline后，其会自动调用本方法
        :param item: Spider每次生成的Item
        :param spider: Spider实例
        :return: 包含数据的字典或Item对象，或抛出DropItem异常
        """
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing Text')


class MongoDBPipeline(object):
    def __init__(self, connection_string, database):
        self.client = None
        self.db = None
        self.connection_string = connection_string
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        """
        一个类方法
        :param crawler: 当前爬虫项目
        :return:
        """
        return cls(
            connection_string=crawler.settings.get('MONGODB_CONNECTION_STRING'),
            database=crawler.settings.get('MONGODB_DATABASE')
        )  # 从当前爬虫的settings.py配置文件中提取

    def open_spider(self, spider):
        """
        数据库连接初始化操作
        当Spider被开启时，本方法被调用
        :param spider: Spider实例
        :return:
        """
        self.client = pymongo.MongoClient(self.connection_string)
        self.db = self.client[self.database]

    def process_item(self, item, spider):
        """
        执行数据插入操作
        :param item: Spider每次生成的Item
        :param spider: Spider实例
        :return:
        """
        name = item.__class__.__name__  # item（对象）所属的类的类名
        self.db[name].insert_one(dict(item))  # 此处的name对应数据库中的collection名（即items.py中定义的QuoteItem）
        return item

    def close_spider(self, spider):
        """
        关闭数据库连接
        当Spider被关闭时，本方法被调用
        :param spider: Spider实例
        :return:
        """
        self.client.close()