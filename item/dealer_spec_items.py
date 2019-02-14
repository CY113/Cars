# -*- coding: utf-8 -*-
import scrapy


class DealerSpecScrapyItem(scrapy.Item):
    dealer_id = scrapy.Field()
    series_id = scrapy.Field()
    spec_id = scrapy.Field()
    series_vr_url = scrapy.Field()
    price = scrapy.Field()
    time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """INSERT INTO auto_home_dealers_spec (dealer_id,series_id,spec_id,price,series_vr_url,update_time) VALUES(%s,%s,%s,%s,%s,str_to_date(%s,'%%Y-%%m-%%d'))
    """
        params = (
            self["dealer_id"], self["series_id"], self["spec_id"], self["price"], self["series_vr_url"], self["time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select id from auto_home_dealers_spec where id =%s"""
        params = (0)
        return query, params
