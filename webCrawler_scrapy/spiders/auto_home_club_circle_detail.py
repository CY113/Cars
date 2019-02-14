# -*- coding: utf-8 -*-


import copy
import json
from scrapy import Request
from scrapy.spiders import CrawlSpider
from models.club import StructureStartUrl
from lib.GetCurrentTime import get_current_date
from item.club_circle_detail_items import ClubCircleDetailScrapyItem


class AutoHomeCircleDetailSpider(CrawlSpider):
    name = "club_circle_detail"
    # club_id_list = [6, 13, 15, 16]
    club_id_list = StructureStartUrl().get_bbs_id()
    # club_id_list = [834]
    club_index = 0
    page_index = 1
    base_url = "https://club.app.autohome.com.cn/club_v8.2.0/club/getcarfriendcirclelist-pm2-utd5a4a902aa6c4db1b5ca0adb2df71dda03f29a2a-b%s-p%s-s20.json"
    start_urls = [base_url % (club_id_list[club_index], page_index)]

    def parse(self, response):
        item = ClubCircleDetailScrapyItem()
        yield Request(url=response.url, callback=self.parse_club_circle_detail_items,
                      meta={"item": copy.deepcopy(item)}, dont_filter=True)

    def parse_club_circle_detail_items(self, response):
        item = response.meta['item']
        content = json.loads(response.body.decode(), strict=False)
        circle_list = content["result"]["list"]
        for circle in circle_list:
            item["bbs_id"] = circle["bbsid"]
            item["circle_id"] = circle["circleid"]
            item["circle_name"] = circle["circlename"]
            item["user_count"] = circle["usercount"]
            item["province_id"] = circle["provinceid"]
            item["city_id"] = circle["cityid"]
            item["explain"] = circle["explain"]
            item["activen_num"] = circle["activennum"]
            item["create_time"] = circle["createtime"]
            item["last_update_time"] = circle["lastupdatetime"]
            item["owner_id"] = circle["ownerid"]
            item["time"] = get_current_date()
            yield item

        self.page_index += 1
        if self.page_index <= content["result"]["pagecount"]:
            print(self.page_index)
            url = self.base_url % (self.club_id_list[self.club_index], self.page_index)
            print(url)
            yield Request(url=url, callback=self.parse_club_circle_detail_items, meta={"item": copy.deepcopy(item)}, dont_filter=True)
        else:
            self.club_index += 1
            if self.club_index < len(self.club_id_list):
                self.page_index = 1
                url = self.base_url % (self.club_id_list[self.club_index], self.page_index)
                yield Request(url=url, callback=self.parse_club_circle_detail_items, meta={"item": copy.deepcopy(item)}, dont_filter=True)
