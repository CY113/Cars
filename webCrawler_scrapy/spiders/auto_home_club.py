# -*- coding: utf-8 -*-

import json
import copy
from scrapy import Request
from scrapy.spiders import CrawlSpider
from item.club_items import ClubScrapyItem


class AutoHomeClubSpider(CrawlSpider):
    name = "club_dict"
    start_urls = ["https://club.app.autohome.com.cn/club_v8.2.0/club/clubsseries-pm2-st636564362160547332.json"]

    def parse(self, response):
        item = ClubScrapyItem()
        yield Request(url=response.url, callback=self.parse_clubs_series_items, meta={"item": copy.deepcopy(item)}, dont_filter=True)

    def parse_clubs_series_items(self, response):
        item = response.meta['item']
        content = json.loads(response.body.decode(), strict=False)
        for letter in content["result"]["list"]:

            for club in letter["seriesclub"]:
                item["brand_name"] = letter["brandname"]
                item["id"] = club["bbsid"]
                item["name"] = club["bbsname"]
                yield item
