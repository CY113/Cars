# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlePvItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """文章列表"""
    article_id = scrapy.Field()  # 文章ID
    pv_count = scrapy.Field()  # 文章标题
    update_time = scrapy.Field()  # 采集时间

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_article_pv (article_id,pv_count,update_time) VALUES (%s, %s, str_to_date(%s,'%%Y-%%m-%%d')) """
        params = (self["article_id"], self["pv_count"], self["update_time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select id from auto_home_article_pv where id =%s"""
        params = (0)
        return query, params
