# -*- coding: utf-8 -*-


import copy
import json
from scrapy import Request
from scrapy.spiders import CrawlSpider
from models.club import StructureStartUrl
from lib.GetCurrentTime import get_current_date
from item.club_topic_list_items import ClubTopicListScrapyItem


class AutoHomeTopicListSpider(CrawlSpider):
    name = "club_topic_list"
    # club_id_list = [6, 13, 15, 16]
    club_id_list = StructureStartUrl().get_bbs_id()
    club_index = 0
    page_index = 1
    base_url = "https://clubnc.app.autohome.com.cn/club_v8.2.0/club/topics-pm2-b%s-btc-r0-ss0-o0-p%s-s50-qf0-c110100-t0-v8.8.0.json"
    start_urls = [base_url % (club_id_list[club_index], page_index)]

    def parse(self, response):
        item = ClubTopicListScrapyItem()
        yield Request(url=response.url, callback=self.parse_club_topic_list_items, meta={"item": copy.deepcopy(item)})

    def parse_club_topic_list_items(self, response):
        item = response.meta['item']
        content = json.loads(response.body.decode(), strict=False)
        topic_list = content["result"]["list"]
        for topic in topic_list:
            item["topic_id"] = topic["topicid"]
            item["bbs_id"] = topic["bbsid"]
            item["title"] = topic["title"]
            item["user_id"] = topic["userid"]
            item["reply_counts"] = topic["replycounts"]
            item["post_topic_date"] = topic["posttopicdate"]
            item["last_reply_date"] = topic["lastreplydate"]
            item["topic_type"] = topic["topictype"]
            item["time"] = get_current_date()
            yield item
        self.page_index += 1
        if self.page_index <= content["result"]["pagecount"]:
            url = self.base_url % (self.club_id_list[self.club_index], self.page_index)
            yield Request(url=url, callback=self.parse_club_topic_list_items, meta={"item": copy.deepcopy(item)},
                          dont_filter=True)
        else:
            self.club_index += 1
            if self.club_index < len(self.club_id_list):
                self.page_index = 1
                url = self.base_url % (self.club_id_list[self.club_index], self.page_index)
                yield Request(url=url, callback=self.parse_club_topic_list_items, meta={"item": copy.deepcopy(item)},
                              dont_filter=True)
