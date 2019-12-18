# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KoubeiTagNumItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    summary_key = scrapy.Field()
    volume = scrapy.Field()
    time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_koubei_tag_num (summary_key, volume,update_time) VALUES (%s, %s,str_to_date(%s,'%%Y-%%m-%%d')) """
        params = (self["summary_key"], self["volume"], self["time"])
        return insert_sql, params

    # 重复入库判断ID=0
    def distinct_data(self):
        query = """select id from auto_home_koubei_tag_num where id=%s"""
        params = (0)
        return query, params