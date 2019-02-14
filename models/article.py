# -*- coding: utf-8 -*-

from lib.dbhelper import DBHelper


class StructureArticleID(object):
    def __init__(self):
        self.db_helper = DBHelper()

    def get_article_id(self):
        article_id_list = []
        sql = """SELECT DISTINCT(id),ver FROM auto_home_article_list ORDER BY  id"""
        for article_id_ver in self.db_helper.query(sql):
            article_id_list.append(article_id_ver)
        article_id_list.sort()
        return article_id_list


if __name__ == "__main__":
    StructureStartUrl = StructureArticleID()
    print(StructureStartUrl.get_article_id()[0][0])
