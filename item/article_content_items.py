# -*- coding: utf-8 -*-


import scrapy


class ArticleContentScrapyItem(scrapy.Item):
    """文章列表"""
    id = scrapy.Field()  # 文章ID
    content = scrapy.Field()  # 文章标题

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_article_content (id,content) VALUES (%s, %s) """
        params = (self["id"], self["content"])
        return insert_sql, params

    def distinct_data(self):
        query = """select id from auto_home_article_content where id =%s"""
        params = (self["id"])
        return query, params
