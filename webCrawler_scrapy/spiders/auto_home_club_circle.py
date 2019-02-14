# -*- coding: utf-8 -*-


import copy
import json
from scrapy import Request
from scrapy.spiders import CrawlSpider
from models.club import StructureStartUrl
from lib.GetCurrentTime import get_current_date
from item.club_circle_items import ClubCircleScrapyItem


class AutoHomeCircleSpider(CrawlSpider):
    name = "club_circle"
    club_id_list = [6, 13, 15, 16]
    club_id_list = StructureStartUrl().get_bbs_id()
    club_index = 0
    base_url = "https://club.app.autohome.com.cn/club_v8.2.0/club/getcarfriendcirclelist-pm2-utd5a4a902aa6c4db1b5ca0adb2df71dda03f29a2a-b%s-p1-s20.json"
    start_urls = [base_url % club_id_list[club_index]]

    def parse(self, response):
        item = ClubCircleScrapyItem()
        yield Request(url=response.url, callback=self.parse_club_circle_items, meta={"item": copy.deepcopy(item)}, dont_filter=True)

    def parse_club_circle_items(self, response):
        item = response.meta['item']
        content = json.loads(response.body.decode(), strict=False)
        result = content["result"]
        item["bbs_id"] = self.club_id_list[self.club_index]
        item["row_count"] = result["rowcount"]
        item["time"] = get_current_date()
        yield item
        self.club_index += 1
        if self.club_index < len(self.club_id_list):
            url = self.base_url % self.club_id_list[self.club_index]
            yield Request(url=url, callback=self.parse_club_circle_items, meta={"item": copy.deepcopy(item)},
                          dont_filter=True)
