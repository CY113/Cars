# -*- coding: utf-8 -*-
import json

import scrapy

from club_topic_info.items import ClubTopicInfoItem
from lib.GetCurrentTime import get_current_date
from models.club import StructureStartUrl


class AutoHomeClubTopicInfoSpider(scrapy.Spider):
    name = 'auto_home_club_topic_info'
    club_id_list = StructureStartUrl().get_bbs_id()
    club_index = 0
    base_url = "https://clubnc.app.autohome.com.cn/club_v8.2.0/club/topics-pm2-b%s-btc-r0-ss0-o0-p2-s50-qf0-c110100-t0-v8.8.0.json"
    start_urls = [base_url % club_id_list[club_index]]

    def parse(self, response):
        item = ClubTopicInfoItem()
        content = json.loads(response.body.decode(), strict=False)
        result = content["result"]
        item["bbs_id"] = result["clubid"]
        item["row_count"] = result["rowcount"]
        item["friend_count"] = result["friendcount"]
        item["time"] = get_current_date()
        yield item
        self.club_index += 1
        if self.club_index < len(self.club_id_list):
            url = self.base_url % self.club_id_list[self.club_index]
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
