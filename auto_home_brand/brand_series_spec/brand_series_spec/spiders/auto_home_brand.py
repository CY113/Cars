# -*- coding: utf-8 -*-
import json
import time
import scrapy

from items.brand_items import BrandScrapyItem


class AutoHomeBrandSpider(scrapy.Spider):
    name = 'auto_home_brand'
    start_urls = ["https://cars.app.autohome.com.cn/cars_v8.7.0/cars/brands-pm2.json?pluginversion=8.7.1"]

    def parse(self, response):
        content = json.loads(response.body.decode())
        item = BrandScrapyItem()
        brand_list = content["result"]["brandlist"]
        for i in range(len(brand_list)):
            for j in range(len(brand_list[i]['list'])):
                item["brand_name"] = brand_list[i]['list'][j]["name"]
                item["brand_id"] = brand_list[i]['list'][j]["id"]
                yield item
                time.sleep(1)
