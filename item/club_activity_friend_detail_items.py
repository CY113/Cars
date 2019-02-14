# -*- coding: utf-8 -*-


import scrapy


class ClubActivityFriendDetailScrapyItem(scrapy.Item):
    """活跃车友详情"""
    bbs_id = scrapy.Field()  # 论坛ID
    user_id = scrapy.Field()  # 活跃车友ID
    recommend = scrapy.Field()  # 是否推荐
    time = scrapy.Field()  # 采集时间

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_club_activity_friend_detail (bbs_id, user_id,recommend,update_time) VALUES (%s, %s,%s, str_to_date(%s,'%%Y-%%m-%%d')) """
        params = (self["bbs_id"], self["user_id"], self["recommend"], self["time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select user_id from auto_home_club_activity_friend_detail where user_id =%s"""
        params = (self["user_id"])
        return query, params
