# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SeriesScrapyItem(scrapy.Item):
    """定义需要格式化的内容（或是需要保存到数据库的字段）"""
    # define the fields for your item here like:
    series_id = scrapy.Field()
    series_name = scrapy.Field()
    brand_id = scrapy.Field()
    level_id = scrapy.Field()
    manufacturer_name = scrapy.Field()
    status = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_series (id, name, brand_id, level_id, 
                        manufacturer_name, status) VALUES (%s, %s, %s, %s, %s, %s) """
        params = (self["series_id"], self["series_name"], self["brand_id"], self["level_id"], self["manufacturer_name"],
                  self["status"])
        return insert_sql, params

    def distinct_data(self):
        query = """select id from auto_home_series where id =%s"""
        params = (self["series_id"])
        return query, params
