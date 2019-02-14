# -*- coding: utf-8 -*-


import scrapy


class KoubeiReadScrapyItem(scrapy.Item):
    """定义需要格式化的内容（或是需要保存到数据库的字段）"""
    # define the fields for your item here like:
    koubei_id = scrapy.Field()
    visit_count = scrapy.Field()
    comment_count = scrapy.Field()
    helpful_count = scrapy.Field()
    time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """INSERT INTO auto_home_koubei_read (id,visit_count,comment_count,helpful_count,update_time) VALUE(%s,%s,%s,%s,str_to_date(%s,'%%Y-%%m-%%d'))
"""
        params = (self["koubei_id"], self["visit_count"], self["comment_count"], self["helpful_count"], self["time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select id from auto_home_koubei_read where id =%s"""
        params = (0)
        return query, params
