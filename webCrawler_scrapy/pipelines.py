# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings
from scrapy import log
import pymysql
import pymysql.cursors
import codecs
import json
import openpyxl
import pymysql


class JsonWithEncodingPipeline(object):
    """保存到文件中对应的class
       1、在settings.py文件中配置
       2、在自己实现的爬虫类中yield item,会自动执行"""

    def __init__(self):
        self.file = codecs.open('info.json', 'w', encoding='utf-8')  # 保存为json文件

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"  # 转为json的
        self.file.write(line)  # 写入文件中
        return item

    def spider_closed(self, spider):  # 爬虫结束时关闭文件
        self.file.close()


class WebcrawlerScrapyPipeline(object):
    """保存到数据库中对应的class
       1、在settings.py文件中配置
       2、在自己实现的爬虫类中yield item,会自动执行"""

    def __init__(self, dbpool):
        self.dbpool = dbpool

        """ 这里注释中采用写死在代码中的方式连接线程池，可以从settings配置文件中读取，更加灵活"""

    @classmethod
    def from_settings(cls, settings):
        """1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法"""
        dbparams = dict(host=settings['MYSQL_HOST'],  # 读取settings中的配置
                        db=settings['MYSQL_DBNAME'], user=settings['MYSQL_USER'], passwd=settings['MYSQL_PASSWD'],
                        charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
                        cursorclass=pymysql.cursors.DictCursor, use_unicode=False, )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    # pipeline默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    # 写入数据库中
    def _conditional_insert(self, tx, item):
        sql, params = item.get_insert_sql()
        return tx.execute(sql, params)

    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print('--------------database operation exception!!-----------------')
        print('-------------------------------------------------------------')
        print(failue)


class ScrapyMySQLPipeline(object):
    def __init__(self):
        self.settings = get_project_settings()
        self.host = self.settings['MYSQL_HOST']
        self.port = self.settings['MYSQL_PORT']
        self.user = self.settings['MYSQL_USER']
        self.passwd = self.settings['MYSQL_PASSWD']
        self.db = self.settings['MYSQL_DBNAME']
        # 连接数据库
        self.connect = pymysql.connect(host=self.host, db=self.db, user=self.user, passwd=self.passwd, charset='utf8',
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
            log(error)
        return item


class ExcelBossPipeline(object):
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.append(['koubei_id', 'viewcount', 'commentcount', 'helpfulcount', 'update_time'])  # 口碑阅读数

    def process_item(self, item, spider):
        line = [item['koubei_id'], item['visit_count'], item['comment_count'], item["helpful_count"], item['time']]
        self.ws.append(line)
        self.wb.save('../data/口碑历史记录.xlsx')  # 保存xlsx文件
        return item
