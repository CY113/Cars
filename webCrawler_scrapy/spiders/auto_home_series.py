# -*- coding: utf-8 -*-

import json
import time
import copy
import scrapy
from scrapy import Request
from item.series_items import SeriesScrapyItem
from models.cars import StructureStartUrl


class AutoHomeSeriesSpider(scrapy.spiders.Spider):
    name = "series"
    brand_list = StructureStartUrl().get_brand_id()
    url_index = 0
    base_url = "https://cars.app.autohome.com.cn/cars_v8.8.5/cars/seriesprice-pm2-b%s-t16-v9.0.0-c110100.json"
    start_urls = [base_url % brand_list[url_index]]

    def parse(self, response):
        result = json.loads(response.body.decode())["result"]
        item = SeriesScrapyItem()
        item["brand_id"] = self.brand_list[self.url_index]
        for fct in result["fctlist"]:  # 在售列表
            manufacturer_name = fct["name"]
            serieslist = fct["serieslist"]
            for series in serieslist:
                item["level_id"] = series["levelid"]
                item["series_name"] = series["name"]
                item["status"] = series["state"]
                item["series_id"] = series["id"]
                item["manufacturer_name"] = manufacturer_name
                yield item
        for other in result["otherfctlist"]:  # 未售/停售
            manufacturer_name = other["name"]
            serieslist = other["serieslist"]
            for series in serieslist:
                item["level_id"] = series["levelid"]
                item["series_name"] = series["name"]
                item["status"] = series["state"]
                item["series_id"] = series["id"]
                item["manufacturer_name"] = manufacturer_name
                yield item
        self.url_index += 1
        if self.url_index < len(self.brand_list):
            url = self.base_url % self.brand_list[self.url_index]
            yield Request(url=url, callback=self.parse, dont_filter=True)
