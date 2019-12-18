# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ClubTopicCommentsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()  # 评论ID
    topic_id = scrapy.Field()  # 帖子ID
    user = scrapy.Field()  # 用户ID
    user_id = scrapy.Field()  # 用户ID
    content = scrapy.Field()  # 发表内容
    publish_time = scrapy.Field()  # 发表时间

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_club_topic_comment(id, topic_id, user_name,user_id,content, publish_time) VALUES (%s, %s, %s, %s, %s, %s) """
        params = (
            self["id"],
            self["topic_id"],
            self["user"],
            self["user_id"],
            self["content"],
            self["publish_time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select id from auto_home_club_topic_comment where id =%s"""
        params = (self['id'])
        return query, params