# Define here the models for your scraped items
# Item是保存爬取数据的容器，定义了爬取结果的数据结构，使用方法和字典类似
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 创建Item需要继承Scrapy的Item类
class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # Field字段即为要爬取的字段
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
