# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ClubScrapyItem(scrapy.Item):
    """定义论坛码表"""
    id = scrapy.Field()  # 论坛ID
    name = scrapy.Field()  # 论坛名字
    brand_name = scrapy.Field()  # 品牌

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_club_dict (bbs_id, bbs_name, brand_name) value (%s, %s, %s)"""
        params = (self['id'], self['name'], self['brand_name'])
        return insert_sql, params

    def distinct_data(self):
        query = """select bbs_id from auto_home_club_dict where bbs_id =%s"""
        params = (self['id'])
        return query, params
