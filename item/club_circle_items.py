# -*- coding: utf-8 -*-


import scrapy


class ClubCircleScrapyItem(scrapy.Item):
    """论坛统计活跃车友数量"""
    bbs_id = scrapy.Field()  # 论坛ID
    row_count = scrapy.Field()  # 车友圈数量
    time = scrapy.Field()  # 采集时间

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_club_circle (bbs_id, row_count,update_time) VALUES (%s, %s,str_to_date(%s,'%%Y-%%m-%%d')) """
        params = (self["bbs_id"], self["row_count"], self["time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select id from auto_home_club_circle where id =%s"""
        params = (0)
        return query, params
