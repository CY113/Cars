# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KoubeiHomeItem(scrapy.Item):
    """定义需要格式化的内容（或是需要保存到数据库的字段）"""
    # define the fields for your item here like:
    koubei_id = scrapy.Field()
    pid = scrapy.Field()
    cid = scrapy.Field()
    dealer_id = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """UPDATE auto_home_koubei SET pid=%s,cid= %s,dealer_id=%s WHERE id = '%s'"""
        params = (self["pid"], self["cid"], self["dealer_id"], self["koubei_id"])
        return insert_sql, params

    def distinct_data(self):
        query = """select id from auto_home_koubei where id =%s"""
        params = (0)
        return query, params
