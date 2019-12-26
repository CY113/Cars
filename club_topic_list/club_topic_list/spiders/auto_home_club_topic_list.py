# -*- coding: utf-8 -*-
import json
import sys

import scrapy
from club_topic_list.items import ClubTopicListItem
from lib.GetCurrentTime import get_current_date
from lib.formmat_time import formmat_time
from models.club import StructureStartUrl


class AutoHomeClubTopicListSpider(scrapy.Spider):
    name = 'auto_home_club_topic_list'
    club_id_list = StructureStartUrl().get_bbs_id()
    # club_id_list = [4744]
    club_index = 0
    page_index = 1
    base_url = "https://clubnc.app.autohome.com.cn/club_v8.2.0/club/topics-pm2-b%s-btc-r0-ss0-o0-p%s-s50-qf0-c110100-t0-v8.8.0.json"
    start_urls = [base_url % (club_id_list[club_index], page_index)]

    def parse(self, response):
        item = ClubTopicListItem()
        content = json.loads(response.body.decode(), strict=False)
        topic_list = content["result"]["list"]
        for topic in topic_list:
            item["topic_id"] = topic["topicid"]
            item["bbs_id"] = topic["bbsid"]
            item["title"] = topic["title"]
            item["user_id"] = topic["userid"]
            item["reply_counts"] = topic["replycounts"]
            post_topic_date = topic["posttopicdate"]
            if "前" in post_topic_date:
                item["post_topic_date"] = formmat_time(post_topic_date)
            else:
                item["post_topic_date"] = post_topic_date
            last_reply_date = topic["lastreplydate"]
            if "前" in post_topic_date:
                item["last_reply_date"] = formmat_time(last_reply_date)
            else:
                item["last_reply_date"] = last_reply_date
            item["topic_type"] = topic["topictype"]
            item["time"] = get_current_date()
            yield item
        self.page_index += 1
        if self.page_index <= content["result"]["pagecount"]:
            url = self.base_url % (self.club_id_list[self.club_index], self.page_index)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
        else:
            self.club_index += 1
            percent = self.club_index / len(self.club_id_list)
            sys.stdout.write("\r" + "抓取进度：%d%%(%d/%d)" % (percent * 100, self.club_index, len(self.club_id_list)))
            if self.club_index < len(self.club_id_list):
                self.page_index = 1
                url = self.base_url % (self.club_id_list[self.club_index], self.page_index)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
