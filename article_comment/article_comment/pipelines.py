# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy import log
from lib.dbhelper import DBHelper


class ArticleCommentPipeline(object):
    def __init__(self):
        self.connect = DBHelper().connectDatabase()
        # 通过cursor执行增删查改
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            sql, params = item.distinct_data()
            self.cursor.execute(sql, params)
            data = self.cursor.fetchone()
            if data:
                pass
            else:
                # 插入数据
                sql, params = item.get_insert_sql()
                self.cursor.execute(sql, params)
                self.connect.commit()

        except Exception as error:
            # 出现错误时打印错误日志
            log(error)
        return item