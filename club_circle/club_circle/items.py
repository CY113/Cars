# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ClubCircleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """论坛统计活跃车友数量"""
    bbs_id = scrapy.Field()  # 论坛ID
    row_count = scrapy.Field()  # 车友圈数量
    targetId = scrapy.Field()  # 车友圈ID
    seriesId = scrapy.Field()  # 车系ID
    score = scrapy.Field()  # 人气
    title = scrapy.Field()  # 车友圈
    explain = scrapy.Field()  # 介绍
    memberCount = scrapy.Field()  # 成员数量
    time = scrapy.Field()  # 采集时间

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_club_circle (bbs_id, row_count,targetId,seriesId,score,title,explains,memberCount,update_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,str_to_date(%s,'%%Y-%%m-%%d')) """
        params = (self["bbs_id"], self["row_count"], self["targetId"],self["seriesId"], self["score"], self["title"],self["explain"], self["memberCount"], self["time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select id from auto_home_club_circle where id =%s"""
        params = (0)
        return query, params
