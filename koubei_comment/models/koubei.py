# coding=utf-8
# @ Author: TianHao
# @ Python: Python3.6.1
# @ Date: 2019/12/17 17:36
# @ Desc
from lib.dbhelper import DBHelper


class StructureStartUrl(object):
    """
    构造分页
    """

    def __init__(self):
        self.db_helper = DBHelper()

    def get_level_id(self):
        level_list = []
        sql = "SELECT id FROM auto_home_level"
        for level_id in self.db_helper.query(sql):
            level_list.append(level_id[0])
        level_list.sort()
        return level_list

    def get_koubei_rand_id(self):
        koubei_rand_list = []
        sql = "SELECT DISTINCT(series_id) FROM auto_home_koubei_rank ORDER BY series_id"
        for series_id in self.db_helper.query(sql):
            koubei_rand_list.append(series_id[0])
        koubei_rand_list.sort()
        return koubei_rand_list
    def get_koubei_id(self):
        koubei_list = []
        sql = 'SELECT id FROM auto_home_koubei WHERE post_time > "2019-01-01"'
        for koubei_id in self.db_helper.query(sql):
            koubei_list.append(koubei_id[0])
        koubei_list.sort()
        return koubei_list

    def get_series_id(self):
        sql = "SELECT DISTINCT(id) FROM auto_home_series ORDER BY id"
        return self.db_helper.query(sql)

    def get_home_koubei_id(self):
        sql = "SELECT DISTINCT(id) FROM auto_home_koubei ORDER BY id"
        return self.db_helper.query(sql)