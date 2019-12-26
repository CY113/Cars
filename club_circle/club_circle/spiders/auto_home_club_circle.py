# -*- coding: utf-8 -*-
import json

import scrapy

from club_circle.items import ClubCircleItem
from lib.GetCurrentTime import get_current_date
from models.club import StructureStartUrl


class AutoHomeClubCircleSpider(scrapy.Spider):
    name = 'auto_home_club_circle'
    club_id_list = StructureStartUrl().get_bbs_id()
    club_index = 0
    page_index = 1
    # base_url = "https://club.app.autohome.com.cn/club_v8.2.0/club/getcarfriendcirclelist-pm2-utd5a4a902aa6c4db1b5ca0adb2df71dda03f29a2a-b%s-p1-s20.json"
    base_url = "https://chat.api.autohome.com.cn/c1/s1/api/getSeriesProvinceTagCyqList?cyqType=1&convertId=%s&memberId=0&pageIndex=%s&pageSize=15&_appid=club.pc"
    start_urls = [base_url % (club_id_list[club_index], page_index)]

    def parse(self, response):
        item = ClubCircleItem()
        content = json.loads(response.body.decode(), strict=False)
        result = content["result"]
        item["bbs_id"] = self.club_id_list[self.club_index]
        item["row_count"] = result["rowCount"]
        details = result["list"]
        pageCount = result["pageCount"]
        for detail in details:
            item["targetId"] = detail["targetId"]  # 车友圈ID
            item["seriesId"] = detail["seriesId"]  # 车系ID
            item["score"] = detail["score"]  # 人气
            item["title"] = detail["title"]  # 车友圈
            item["explain"] = detail["explain"]  # 介绍
            item["memberCount"] = detail["memberCount"]  # 成员数量
            item["time"] = get_current_date()
            yield item
        self.page_index += 1
        if self.page_index < pageCount:
            url = self.base_url % (self.club_id_list[self.club_index], self.page_index)
            yield scrapy.Request(url, callback=self.parse)
        else:
            self.club_index += 1
            if self.club_index < len(self.club_id_list):
                self.page_index = 1
                url = self.base_url % (self.club_id_list[self.club_index], self.page_index)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
