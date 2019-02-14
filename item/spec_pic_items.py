# -*- coding: utf-8 -*-

import scrapy


class SpecPicScrapyItem(scrapy.Item):
    """定义需要格式化的内容（或是需要保存到数据库的字段）"""
    # define the fields for your item here like:
    pic_id = scrapy.Field()
    type_id = scrapy.Field()
    spec_id = scrapy.Field()
    share_url = scrapy.Field()
    big_pic = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_spec_pic (id, type_id, spec_id, share_url, big_pic) VALUES (%s, %s, %s, %s, %s) """
        params = (self["pic_id"], self["type_id"], self["spec_id"], self["share_url"], self["big_pic"])
        return insert_sql, params
