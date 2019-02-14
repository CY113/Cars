# -*- coding: utf-8 -*-

import scrapy


class ClubTopicReadScrapyItem(scrapy.Item):
    """帖子阅读数"""
    topic_id = scrapy.Field()  # 帖子ID
    reply = scrapy.Field()  # 回复帖子数
    view = scrapy.Field()  # 阅读数
    time = scrapy.Field()  # 采集时间

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_club_topic_read (topic_id, reply, view, update_time) VALUES (%s, %s, %s ,str_to_date(%s,'%%Y-%%m-%%d') ) """
        params = (self["topic_id"], self["reply"], self["view"], self["time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select id from auto_home_club_topic_read where id =%s"""
        params = (0)
        return query, params
