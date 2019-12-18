# -*- coding: utf-8 -*-
import json
import scrapy

from club_activity_friends_details.items import ClubActivityFriendsDetailsItem
from lib.GetCurrentTime import get_current_date
from models.club import StructureStartUrl


class AutoHomeClubActivityFriendsDetailsSpider(scrapy.Spider):
    name = 'auto_home_club_activity_friends_details'
    club_id_list = StructureStartUrl().get_bbs_id()
    club_index = 0
    page_index = 1
    base_url = "https://club.app.autohome.com.cn/club_v8.2.0/club/getactivityfriendlist-pm2-b%s-t2-c0-u66230826-p%s-s20.json"
    start_urls = [base_url % (club_id_list[club_index], page_index)]

    def parse(self, response):
        item = ClubActivityFriendsDetailsItem()
        content = json.loads(response.body.decode(), strict=False)
        activity_friend_list = content["result"]["activityfriendlist"]  # 活跃车友
        club_master_list = content["result"]["clubmasterlist"]  # 推荐车友
        for club_master in club_master_list:
            item["bbs_id"] = self.club_id_list[self.club_index]
            item["user_id"] = club_master["userid"]
            item["recommend"] = 0
            item["time"] = get_current_date()
            yield item
        for activity_friend in activity_friend_list:
            item["bbs_id"] = self.club_id_list[self.club_index]
            item["user_id"] = activity_friend["userid"]
            item["recommend"] = 1
            item["time"] = get_current_date()
            yield item

        self.page_index += 1
        if self.page_index <= content["result"]["pagecount"]:
            print(self.page_index)
            url = self.base_url % (self.club_id_list[self.club_index], self.page_index)
            print(url)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
        else:
            self.club_index += 1
            if self.club_index < len(self.club_id_list):
                self.page_index = 1
                url = self.base_url % (self.club_id_list[self.club_index], self.page_index)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

