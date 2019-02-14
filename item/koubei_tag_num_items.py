# -*- coding: utf-8 -*-

import scrapy


class KoubeiTagNumItem(scrapy.Item):
    summary_key = scrapy.Field()
    volume = scrapy.Field()
    time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_koubei_tag_num (summary_key, volume,update_time) VALUES (%s, %s,str_to_date(%s,'%%Y-%%m-%%d')) """
        params = (self["summary_key"], self["volume"], self["time"])
        return insert_sql, params

    # 重复入库判断ID=0
    def distinct_data(self):
        query = """select id from auto_home_koubei_tag_num where id=%s"""
        params = (0)
        return query, params
