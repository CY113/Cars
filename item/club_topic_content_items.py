# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ClubTopicContentItem(scrapy.Item):
    """定义帖子内容"""
    topic_id = scrapy.Field()  # 帖子ID
    content = scrapy.Field()  # 发表内容

    # def get_insert_sql(self):
    #     insert_sql = """insert into auto_home_brand (id, name) VALUES (%s, %s) """
    #     params = (self["brand_id"], self["brand_name"])
    #     return insert_sql, params
