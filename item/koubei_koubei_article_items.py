# -*- coding: utf-8 -*-


import scrapy


class KoubeiArticleScrapyItem(scrapy.Item):
    """定义需要格式化的内容（或是需要保存到数据库的字段）"""
    # define the fields for your item here like:
    koubei_id = scrapy.Field()
    feeling_name = scrapy.Field()
    feeling = scrapy.Field()
    score = scrapy.Field()
    time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """INSERT INTO auto_home_koubei_article (koubei_id,feeling_name,feeling,score,update_time) VALUE(%s,%s,%s,%s,str_to_date(%s,'%%Y-%%m-%%d'))
"""
        params = (self["koubei_id"], self["feeling_name"], self["feeling"], self["score"], self["time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select koubei_id from auto_home_koubei_article where koubei_id =%s"""
        params = (self["koubei_id"])
        return query, params
