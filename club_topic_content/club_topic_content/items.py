# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ClubTopicContentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    topic_id = scrapy.Field()  # 帖子ID
    content = scrapy.Field()  # 发表内容

    def get_insert_sql(self):
        insert_sql = "insert into auto_home_club_topic_content(topic_id,content) values (%s,%s)"
        params = (self["topic_id"], self["content"])
        return insert_sql, params
