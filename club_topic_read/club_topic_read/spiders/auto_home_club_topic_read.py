# -*- coding: utf-8 -*-
import json
import re

import scrapy

from club_topic_read.items import ClubTopicReadItem
from lib.GetCurrentTime import get_current_date
from models.club import StructureStartUrl


class AutoHomeClubTopicReadSpider(scrapy.Spider):
    name = 'auto_home_club_topic_read'
    topic_id_list = StructureStartUrl().get_topic_id()
    topic_index = 0
    base_url = "https://forum.app.autohome.com.cn/forum_v7.9.5/forum/club/topicaddclicksajax?topicid=%s"
    start_urls = [base_url % topic_id_list[topic_index]]

    def parse(self, response):
        item = ClubTopicReadItem()
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
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
