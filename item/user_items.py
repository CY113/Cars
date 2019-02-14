# -*- coding: utf-8 -*-

import scrapy


class UserScrapyItem(scrapy.Item):
    """定义需要格式化的内容（或是需要保存到数据库的字段）"""
    # define the fields for your item here like:
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    user_sex = scrapy.Field()
    user_regtime = scrapy.Field()
    user_pid = scrapy.Field()
    user_cid = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_user (user_id, name, sex, regtime, pid, cid) VALUES (%s, %s, %s, %s, %s,%s) """
        params = (self["user_id"], self["user_name"], self["user_sex"], self["user_regtime"], self["user_pid"],self["user_cid"])
        return insert_sql, params
