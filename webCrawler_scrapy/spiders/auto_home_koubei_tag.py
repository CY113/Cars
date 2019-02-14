# -*- coding: utf-8 -*-

import json
import scrapy
import copy
from models.koubei import StructureStartUrl
from item.koubei_tag_items import KoubeiTagItems
from scrapy import Request


class AutoHomeKoubeiTagSpider(scrapy.spiders.Spider):
    name = "koubei_tag"
    series_list = StructureStartUrl().get_series_id()
    base_url = "https://koubei.app.autohome.com.cn/autov8.6.5/alibi/seriesalibiinfos-pm2-ss%s-st0-p1-s20-isstruct1-o0.json"
    series_index = 0
    start_urls = [base_url % series_list[series_index][0]]

    def parse(self, response):
        item = KoubeiTagItems()
        yield Request(url=response.url, callback=self.parse_tag_item, meta={'item': copy.deepcopy(item)},
                      dont_filter=True)

    def parse_tag_item(self, response):
        item = response.meta["item"]
        content = json.loads(response.body.decode(), strict=False)
        result = content["result"]
        if len(result["structuredlist"]) > 0:
            for structure in result["structuredlist"]:
                item["series_id"] = self.series_list[self.series_index][0]
                item["tag_id"] = structure["id"]
                for summary in structure["Summary"]:
                    if summary["SummaryKey"] != 0:
                        item["combination"] = summary["Combination"]
                        item["summary_key"] = summary["SummaryKey"]
                        yield item

        self.series_index += 1
        if self.series_index < len(self.series_list):
            url = self.base_url % self.series_list[self.series_index][0]
            yield Request(url=url, callback=self.parse_tag_item, meta={'item': copy.deepcopy(item)}, dont_filter=True)
