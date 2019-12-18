# -*- coding: utf-8 -*-
import json
import re

import scrapy
from scrapy import Request

from items.spec_items import SpecScrapyItem
from models.cars import StructureStartUrl


class AutoHomeSpecSpider(scrapy.spiders.Spider, StructureStartUrl):
    name = "auto_home_spec"
    series_list = StructureStartUrl().get_series_id()
    url_index = 0
    base_url = "https://cars.app.autohome.com.cn/carinfo_v8.6.0/cars/seriessummary-pm2-s%s-t-c110100-v8.7.1.json?pluginversion=8.7.1"
    start_urls = [base_url % series_list[url_index]]

    def parse(self, response):
        result = json.loads(response.body.decode())["result"]
        item = SpecScrapyItem()
        series_id = re.search('s\d+', response.url).group()
        for engine in result["enginelist"]:
            if engine["yearname"] != "全部在售":
                for yearspec in engine["yearspeclist"]:
                    for spec in yearspec["speclist"]:
                        item["spec_id"] = spec["id"]
                        item["spec_name"] = spec["name"]
                        item["spec_price"] = spec["price"].rstrip("万")
                        item["spec_status"] = spec["state"]
                        item["series_id"] = series_id.lstrip("s")
                        yield item

        self.url_index += 1
        if self.url_index < len(self.series_list):
            url = self.base_url % self.series_list[self.url_index]
            yield Request(url=url, callback=self.parse, dont_filter=True)
