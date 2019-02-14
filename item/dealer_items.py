# -*- coding: utf-8 -*-
import scrapy


class DealerScrapyItem(scrapy.Item):
    """定义需要格式化的内容（或是需要保存到数据库的字段）"""
    # define the fields for your item here like:
    dealer_id = scrapy.Field()
    dealer_city = scrapy.Field()
    company = scrapy.Field()
    company_simple = scrapy.Field()
    address = scrapy.Field()
    pid = scrapy.Field()
    cid = scrapy.Field()
    sid = scrapy.Field()
    business_area = scrapy.Field()
    lon = scrapy.Field()
    lat = scrapy.Field()
    kind_id = scrapy.Field()
    star_level = scrapy.Field()
    update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_dealer (id, name, short_name, kind_id, address,pid,cid,sid,business_area,update_time,lat,lon) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, str_to_date(%s,'%%Y-%%m-%%d'),%s,%s) """
        params = (
            self["dealer_id"], self["company"], self["company_simple"], self["kind_id"], self["address"], self["pid"],
            self["cid"], self["sid"], self["business_area"], self["update_time"], self["lat"], self["lon"])
        return insert_sql, params

    def distinct_data(self):
        query = """select id from auto_home_dealer where id =%s"""
        params = (self["dealer_id"])
        return query, params
