# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ClubTopicCommentScrapyItem(scrapy.Item):
    """定义帖子内容"""
    id = scrapy.Field()  # 评论ID
    topic_id = scrapy.Field()  # 帖子ID
    user = scrapy.Field()  # 用户ID
    content = scrapy.Field()  # 发表内容
    publish_time = scrapy.Field()  # 发表时间

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_club_topic_comment (id, topic_id, user_name, content, publish_time) VALUES (%s, %s, %s, %s, %s) """
        params = (self["id"], self["topic_id"], self["user"], self["content"], self["publish_time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select id from auto_home_club_topic_comment where id =%s"""
        params = (self['id'])
        return query, params
