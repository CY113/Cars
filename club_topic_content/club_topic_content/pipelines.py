# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from lib.dbhelper import DBHelper


class ClubTopicContentPipeline(object):
    def __init__(self):
        self.connect = DBHelper().connectDatabase()
        # 连接数据库
        self.connect = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                               charset='utf8')

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            # 插入数据
            sql, params = item.get_insert_sql()
            self.cursor.execute(sql, params)
            self.connect.commit()

        except Exception as error:
            # 出现错误时打印错误日志
            print(error)
        return item
