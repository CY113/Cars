# -*- coding: utf-8 -*-


import scrapy


class UserCarsScrapyItem(scrapy.Item):
    """定义需要格式化的内容（或是需要保存到数据库的字段）"""
    # define the fields for your item here like:
    user_id = scrapy.Field()
    spec_id = scrapy.Field()
    cert_date = scrapy.Field()
    time = scrapy.Field()
