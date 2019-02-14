# -*- coding: utf-8 -*-

from lib.dbhelper import DBHelper


class StructureStartUrl(object):
    """
    构造分页
    """

    def __init__(self):
        self.db_helper = DBHelper()

    def get_dealer_id(self):
        dealer_id_list = []
        sql = "SELECT DISTINCT(id) FROM auto_home_dealer"
        for bbs_id in self.db_helper.query(sql):
            dealer_id_list.append(bbs_id[0])
        dealer_id_list.sort()
        return dealer_id_list
