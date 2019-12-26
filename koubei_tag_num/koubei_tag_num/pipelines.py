# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from lib.DBHelper import DBHelper

class KoubeiTagNumPipeline(object):
    def __init__(self):
        self.db_helper = DBHelper()
        # 连接数据库
        self.connect = pymysql.connect(host=self.host, db=self.db, user=self.user, passwd=self.passwd,
                                       charset='utf8',
                                       port=self.port,
                                       use_unicode=False)

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
            print(error)
        return item

        
