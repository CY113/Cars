# -*- coding: utf-8 -*-
import json

import scrapy

from club_activity_friends.items import ClubActivityFriendsItem
from lib.GetCurrentTime import get_current_date
from models.club import StructureStartUrl


class AutoHomeClubActivityFriendsSpider(scrapy.Spider):
    name = 'auto_home_club_activity_friends'
    club_id_list = StructureStartUrl().get_bbs_id()
    club_index = 0
    base_url = "https://club.app.autohome.com.cn/club_v8.2.0/club/getactivityfriendlist-pm2-b%s-t2-c0-u66230826-p1-s20.json"
    start_urls = [base_url % club_id_list[club_index]]

    def parse(self, response):
        item = ClubActivityFriendsItem()
        content = json.loads(response.body.decode(), strict=False)
        result = content["result"]
        item["bbs_id"] = self.club_id_list[self.club_index]
        item["activity_friend_count"] = result["activityfriendcount"]
        item["time"] = get_current_date()
        yield item
        self.club_index += 1
        if self.club_index < len(self.club_id_list):
            url = self.base_url % self.club_id_list[self.club_index]
            yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)
