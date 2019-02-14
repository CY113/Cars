# -*- coding: utf-8 -*-


import scrapy


class ArticleListScrapyItem(scrapy.Item):
    """文章列表"""
    id = scrapy.Field()  # 文章ID
    title = scrapy.Field()  # 文章标题
    media_type = scrapy.Field()  # 媒体类型
    type = scrapy.Field()  # 媒体类型
    publish_time = scrapy.Field()  # 发布时间
    author = scrapy.Field()  # 作者
    ver = scrapy.Field()
    update_time = scrapy.Field()  # 采集时间
    last_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_article_list (id,title,media_type,type,publish_time,author,ver,update_time) VALUES (%s, %s, %s, %s, %s, %s, %s, str_to_date(%s,'%%Y-%%m-%%d')) """
        params = (self["id"], self["title"], self["media_type"], self["type"], self["publish_time"], self["author"],
                  self["ver"], self["update_time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select id from auto_home_article_list where id =%s"""
        params = (self["id"])
        return query, params
