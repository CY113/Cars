# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KoubeiTagItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    series_id = scrapy.Field()
    tag_id = scrapy.Field()
    summary_key = scrapy.Field()
    combination = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_koubei_tag (series_id, summary_key,combination,category) VALUES (%s, %s, %s, %s) """
        params = (self["series_id"], self["summary_key"], self["combination"], self["tag_id"])
        return insert_sql, params

    # 根据summary_key判断数据库是否包含combination
    def distinct_data(self):
        query = """select summary_key from auto_home_koubei_tag where summary_key =%s"""
        params = (self["summary_key"])
        return query, params
