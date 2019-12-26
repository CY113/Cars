# coding=utf-8
# @ Author: TianHao
# @ Python: Python3.6.1
# @ Date: 2019/10/29 10:29
# @ Desc

from lib.dbhelper import DBHelper


class StructureStartUrl(object):
    """
    构造分页
    """

    def __init__(self):
        self.db_helper = DBHelper()

    def get_bbs_id(self):
        bbs_id_list = []
        sql = "SELECT bbs_id FROM auto_home_club_dict"
        for bbs_id in self.db_helper.query(sql):
            bbs_id_list.append(bbs_id[0])
        bbs_id_list.sort()
        return bbs_id_list

    def get_topic_id(self):
        topic_id_list = []
        sql = "SELECT DISTINCT(topic_id) FROM `auto_home_club_topic_list` WHERE post_topic_date >= '2018-01-01' ORDER BY topic_id"
        # sql = "SELECT DISTINCT(topic_id) FROM `auto_home_club_topic_list` WHERE post_topic_date >= '2018-01-01' and topic_id>70324364 ORDER BY topic_id"
        for topic_id in self.db_helper.query(sql):
            topic_id_list.append(topic_id[0])
        topic_id_list.sort()
        return topic_id_list

    def get_bbs_topic_id(self):
        sql = 'SELECT bbs_id,topic_id FROM auto_home_club_topic_list WHERE post_topic_date > "2018-01-01" ORDER BY topic_id '
        topic_id_list = DBHelper().query(sql)
        return topic_id_list

if __name__ == "__main__":
    StructureStartUrl = StructureStartUrl()
    print(StructureStartUrl.get_topic_id())