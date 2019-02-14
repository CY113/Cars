# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KoubeiScrapyItem(scrapy.Item):
    """定义需要格式化的内容（或是需要保存到数据库的字段）"""
    # define the fields for your item here like:
    koubei_id = scrapy.Field()
    spec_id = scrapy.Field()
    user_id = scrapy.Field()
    buy_price = scrapy.Field()
    post_time = scrapy.Field()
    # pid = scrapy.Field()
    # cid = scrapy.Field()
    # dealer_id = scrapy.Field()
    page_num = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """INSERT INTO auto_home_koubei (id,spec_id,user_id,buy_price,post_time) VALUE(%s,%s,%s,%s,str_to_date(%s,'%%Y-%%m-%%d'))"""
        params = (self["koubei_id"], self["spec_id"], self["user_id"], self["buy_price"], self["post_time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select id from auto_home_koubei where id =%s"""
        params = (self["koubei_id"])
        return query, params
