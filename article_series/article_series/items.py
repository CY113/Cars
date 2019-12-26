# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleSeriesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    ver = scrapy.Field()
    page_id = scrapy.Field()
    series_id = scrapy.Field()
    series_name = scrapy.Field()
    pv_count = scrapy.Field()

    def get_insert_sql(self):
        """入库文章相关的车系"""
        insert_sql = """INSERT INTO auto_home_article_series (article_id,series_id) VALUES (%s, %s) """
        params = (self["id"], self["series_id"])
        return insert_sql, params

    def distinct_data(self):
        """检测数据是否存在"""
        query = """select id from auto_home_article_series where article_id =%s and series_id = %s"""
        params = (self["id"], self["series_id"])
        return query, params
