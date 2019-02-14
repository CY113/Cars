# -*- coding: utf-8 -*-

from lib.dbhelper import DBHelper


class StructureStartUrl(object):
    """
    构造分页
    """

    def __init__(self):
        self.db_helper = DBHelper()

    def get_brand_id(self):
        brand_list = []
        sql = "select id from auto_home_brand"
        for brand_id in self.db_helper.query(sql):
            brand_list.append(brand_id[0])
        brand_list.sort()
        return brand_list

    def get_series_id(self):
        series_list = []
        sql = "select id from auto_home_series"
        for series_id in self.db_helper.query(sql):
            series_list.append(series_id[0])
        series_list.sort()
        return series_list


if __name__ == "__main__":
    StructureStartUrl = StructureStartUrl()
    print(len(StructureStartUrl.get_bbs_id()))
