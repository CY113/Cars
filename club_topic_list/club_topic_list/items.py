# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ClubTopicListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """定义论坛帖子信息"""
    topic_id = scrapy.Field()  # 帖子ID
    bbs_id = scrapy.Field()  # 论坛ID
    title = scrapy.Field()  # 帖子标题
    user_id = scrapy.Field()  # 作者
    reply_counts = scrapy.Field()  # 帖子回复数
    post_topic_date = scrapy.Field()  # 发布时间
    last_reply_date = scrapy.Field()  # 最后回帖时间
    topic_type = scrapy.Field()  # 帖子的类型
    time = scrapy.Field()  # 采集时间

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_club_topic_list (topic_id, bbs_id, title, user_id,reply_counts, post_topic_date, last_reply_date, topic_type, update_time) VALUES (%s, %s,%s, %s,%s, %s,%s, %s, str_to_date(%s,'%%Y-%%m-%%d')) """
        params = (self["topic_id"], self["bbs_id"], self["title"], self["user_id"], self["reply_counts"],
                  self["post_topic_date"], self["last_reply_date"], self["topic_type"], self["time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select topic_id from auto_home_club_topic_list where topic_id =%s"""
        params = (self["topic_id"])
        return query, params
