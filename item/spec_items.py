# -*- coding: utf-8 -*-
import scrapy


class SpecScrapyItem(scrapy.Item):
    """定义需要格式化的内容（或是需要保存到数据库的字段）"""
    # define the fields for your item here like:
    spec_id = scrapy.Field()
    spec_name = scrapy.Field()
    series_id = scrapy.Field()
    spec_price = scrapy.Field()
    spec_status = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_spec (id, name, series_id, price, status) VALUES (%s, %s, %s, %s, %s) """
        params = (self["spec_id"], self["spec_name"], self["series_id"], self["spec_price"], self["spec_status"])
        return insert_sql, params

    def distinct_data(self):
        query = """select id from auto_home_spec where id =%s"""
        params = (self["spec_id"])
        return query, params
