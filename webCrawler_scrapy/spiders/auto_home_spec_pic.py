# -*- coding: utf-8 -*-


import json
import copy
import time
import scrapy
from item.spec_pic_items import SpecPicScrapyItem
from models.cars import StructureStartUrl
from scrapy import Request


#
class AutoHomeSpecPicSpider(scrapy.spiders.Spider):
    name = "spec_pic"
    url_index = 0
    page_index = 1
    series_list = StructureStartUrl().get_series_id()
    base_url = "https://cars.app.autohome.com.cn/carinfo_v8.7.5/cars/pics-pm2-ss%s-sp0-cg1-cl0-p%s-s60-isn0-ft1-v8.7.6.json?pluginversion=8.7.6"
    start_urls = [base_url % (series_list[url_index], page_index)]

    def parse(self, response):
        item = SpecPicScrapyItem()
        print(response.url)
        yield Request(url=response.url, callback=self.parse_pic_item, meta={"item": copy.deepcopy(item)})

    def parse_pic_item(self, response):
        result = json.loads(response.body.decode())["result"]
        item = response.meta['item']
        pic_list = result["piclist"]
        for pic in pic_list:
            item["pic_id"] = pic["id"]
            item["big_pic"] = pic["bigpic"]
            item["share_url"] = pic["shareurl"]
            item["spec_id"] = pic["specid"]
            item["type_id"] = pic["typeid"]
            yield item
            self.page_index += 1
            if self.page_index <= result["pagecount"]:
                url = self.base_url % (self.series_list[self.url_index], self.page_index)
                yield Request(url=url, callback=self.parse_pic_item, meta={"item": copy.deepcopy(item)}, dont_filter=True)
            else:
                self.url_index += 1
                if self.url_index < len(self.series_list):
                    self.page_index = 1
                    url = self.base_url % (self.series_list[self.url_index], self.page_index)
                    print(url)
                    yield Request(url=url, callback=self.parse_pic_item, meta={"item": copy.deepcopy(item)},
                                  dont_filter=True)
