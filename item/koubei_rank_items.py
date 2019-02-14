# -*- coding: utf-8 -*-
import scrapy


class KoubeiRankScrapyItem(scrapy.Item):
    """定义需要格式化的内容（或是需要保存到数据库的字段）"""
    # define the fields for your item here like:
    level_id = scrapy.Field()
    series_id = scrapy.Field()
    koubei_rank = scrapy.Field()
    koubei_score = scrapy.Field()
    koubei_evaluation_count = scrapy.Field()
    koubei_update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """insert into auto_home_koubei_rank (level_id,series_id,rank,score, evaluation_count,update_time) VALUES (%s,%s,%s,%s,%s,str_to_date(%s,'%%Y-%%m-%%d')) """
        params = (
        self["level_id"], self["series_id"], self["koubei_rank"], self["koubei_score"], self["koubei_evaluation_count"],
        self["koubei_update_time"])
        return insert_sql, params

    def distinct_data(self):
        query = """select id from auto_home_koubei_rank where id =%s"""
        params = (0)
        return query, params
