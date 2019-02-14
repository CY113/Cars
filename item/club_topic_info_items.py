# -*- coding: utf-8 -*-


import scrapy


class ClubTopicInfoScrapyItem(scrapy.Item):
    """论坛信息(用户数、帖子数)"""
    bbs_id = scrapy.Field()  # 论坛ID
    row_count = scrapy.Field()  # 帖子数量
    friend_count = scrapy.Field()  # 车友数
    time = scrapy.Field()  # 采集时间

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_club_topic_info (bbs_id,row_count,friend_count,update_time) VALUES (%s, %s, %s, str_to_date(%s,'%%Y-%%m-%%d')) """
        params = (self["bbs_id"], self["row_count"], self["friend_count"], self["time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select id from auto_home_club_topic_info where id =%s"""
        params = (0)
        return query, params
