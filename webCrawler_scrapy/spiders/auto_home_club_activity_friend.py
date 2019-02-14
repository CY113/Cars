# -*- coding: utf-8 -*-


import copy
import json
from scrapy import Request
from scrapy.spiders import CrawlSpider
from lib.GetCurrentTime import get_current_date
from models.club import StructureStartUrl
from item.club_activity_friend_items import ClubActivityFriendScrapyItem


class AutoHomeClubActivityFriendSpider(CrawlSpider):
    name = "club_activity_friend"
    # club_id_list = [6, 13, 15, 16]
    club_id_list = StructureStartUrl().get_bbs_id()
    club_index = 0
    base_url = "https://club.app.autohome.com.cn/club_v8.2.0/club/getactivityfriendlist-pm2-b%s-t2-c0-u66230826-p1-s20.json"
    start_urls = [base_url % club_id_list[club_index]]

    def parse(self, response):
        item = ClubActivityFriendScrapyItem()
        yield Request(url=response.url, callback=self.parse_club_activity_friend_items, meta={"item": copy.deepcopy(item)}, dont_filter=True)

    def parse_club_activity_friend_items(self, response):
        item = response.meta['item']
        content = json.loads(response.body.decode(), strict=False)
        result = content["result"]
        item["bbs_id"] = self.club_id_list[self.club_index]
        item["activity_friend_count"] = result["activityfriendcount"]
        item["time"] = get_current_date()
        yield item
        self.club_index += 1
        if self.club_index < len(self.club_id_list):
            url = self.base_url % self.club_id_list[self.club_index]
            yield Request(url=url, callback=self.parse_club_activity_friend_items, meta={"item": copy.deepcopy(item)}, dont_filter=True)
