# -*- coding: utf-8 -*-

import re
import copy
import json
from scrapy import Request
from scrapy.spiders import CrawlSpider
from models.club import StructureStartUrl
from lib.GetCurrentTime import get_current_date
from item.club_topic_read_items import ClubTopicReadScrapyItem


class AutoHomeTopicReadSpider(CrawlSpider):
    """帖子的阅读数"""
    name = "club_topic_read"
    # topic_id_list = [1570, 2715, 3246]
    offset = 0
    topic_id_list = StructureStartUrl().get_topic_id(offset)
    topic_index = 0
    base_url = "https://forum.app.autohome.com.cn/forum_v7.9.5/forum/club/topicaddclicksajax?topicid=%s"
    start_urls = [base_url % topic_id_list[topic_index]]

    def parse(self, response):
        item = ClubTopicReadScrapyItem()
        yield Request(url=response.url, callback=self.parse_club_topic_read_items, meta={"item": copy.deepcopy(item)},
                      dont_filter=True)

    def parse_club_topic_read_items(self, response):
        item = response.meta['item']
        content = response.body.decode()
        content = re.search(r"{[^}]+}", content).group()
        content = json.loads(content, strict=False)
        item["topic_id"] = content["TopicId"]
        item["reply"] = content["Replys"]
        item["view"] = content["Views"]
        item["time"] = get_current_date()
        yield item
        self.topic_index += 1
        if self.topic_index < len(self.topic_id_list):
            url = self.base_url % self.topic_id_list[self.topic_index]
            yield Request(url=url, callback=self.parse_club_topic_read_items, meta={"item": copy.deepcopy(item)},
                          dont_filter=True)
        else:
            self.offset += 1000
            self.topic_id_list = StructureStartUrl().get_topic_id(self.offset)
            if 1000 >= len(self.topic_id_list) > 0:
                self.topic_index = 0
                print(self.topic_id_list[self.topic_index])
                url = self.base_url % self.topic_id_list[self.topic_index]
                yield Request(url=url, callback=self.parse_club_topic_read_items, meta={"item": copy.deepcopy(item)},
                              dont_filter=True)
