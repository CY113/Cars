# -*- coding: utf-8 -*-
import scrapy


class ArticleCommentScrapyItem(scrapy.Item):
    """文章列表"""
    article_id = scrapy.Field()  # 文章ID
    comment_id = scrapy.Field()  # 评论ID
    floor = scrapy.Field()  # 楼层
    user_id = scrapy.Field()  # 用户
    publish_time = scrapy.Field()  # 发布时间
    content = scrapy.Field()  # 评论内容
    update_time = scrapy.Field()  # 采集时间

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_article_comment (article_id,comment_id,floor,user_id,publish_time,content,update_time) VALUES (%s, %s, %s, %s, %s, %s, str_to_date(%s,'%%Y-%%m-%%d')) """
        params = (self["article_id"], self["comment_id"], self["floor"], self["user_id"], self["publish_time"],
                  self["content"], self["update_time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select comment_id from auto_home_article_comment where comment_id =%s"""
        params = (self["comment_id"])
        return query, params
