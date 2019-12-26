# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KoubeiArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    koubei_id = scrapy.Field()
    feeling_name = scrapy.Field()
    feeling = scrapy.Field()
    score = scrapy.Field()
    time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """INSERT INTO auto_home_koubei_article (koubei_id,feeling_name,feeling,score,update_time) VALUE(%s,%s,%s,%s,str_to_date(%s,'%%Y-%%m-%%d'))"""
        params = (self["koubei_id"], self["feeling_name"], self["feeling"], self["score"], self["time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select koubei_id from auto_home_koubei_article where koubei_id =%s"""
        params = (self["koubei_id"])
        return query, params
