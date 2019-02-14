# -*- coding: utf-8 -*-


import scrapy


class ClubCircleDetailScrapyItem(scrapy.Item):
    """活跃车友详情"""
    bbs_id = scrapy.Field()  # 论坛ID
    circle_id = scrapy.Field()  # 车友圈ID
    circle_name = scrapy.Field()  # 车友圈名字
    user_count = scrapy.Field()  # 车友圈用户
    province_id = scrapy.Field()  # 车友圈身份
    city_id = scrapy.Field()  # 城市
    explain = scrapy.Field()  # 说明
    activen_num = scrapy.Field()
    create_time = scrapy.Field()  # 创建时间
    last_update_time = scrapy.Field()  # 最后更新时间
    owner_id = scrapy.Field()  # 车友会群主ID
    time = scrapy.Field()  # 采集时间

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_club_circle_detail (bbs_id, circle_id, circle_name, user_count, province_id, city_id, `explain`, activen_num, create_time, last_update_time, owner_id,update_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,str_to_date(%s,'%%Y-%%m-%%d')) """
        params = (self["bbs_id"], self["circle_id"], self["circle_name"], self["user_count"], self["province_id"],
                  self["city_id"], self["explain"], self["activen_num"], self["create_time"], self["last_update_time"],
                  self["owner_id"], self["time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select circle_id from auto_home_club_circle_detail where circle_id =%s"""
        params = (self["circle_id"])
        return query, params
