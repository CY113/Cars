# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KoubeiCommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    koubei_id = scrapy.Field()
    id = scrapy.Field()
    user_id = scrapy.Field()
    content = scrapy.Field()
    create_time = scrapy.Field()
    time = scrapy.Field()
    carname = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """INSERT INTO auto_home_koubei_comment (id,koubei_id,user_id,content,create_time,carname,update_time) VALUE(%s,%s,%s,%s,%s,%s,str_to_date(%s,'%%Y-%%m-%%d'))"""
        params = (self["id"], self["koubei_id"], self["user_id"], self["content"], self["create_time"], self["carname"],
                  self["time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select id from auto_home_koubei_comment where id =%s"""
        params = (self["id"])
        return query, params
