# -*- coding: utf-8 -*-

import re
import copy
import json
import scrapy
from scrapy import Request
from item.dealer_spec_items import DealerSpecScrapyItem
from models.dealer import StructureStartUrl
from lib.GetCurrentTime import get_current_date


class AutoHomeDealerSpecSpider(scrapy.spiders.Spider):
    name = "dealer_spec"
    base_url = "https://dealerframe.m.autohome.com.cn/dealerm/ajax/GetFacSeriesInfoByDealerId?dealerId=%s"
    spec_base_url = "https://dealerframe.m.autohome.com.cn/dealerm/price/GetSeriesSpecs?dealerId=%s&seriesId=%s"
    dealer_list = StructureStartUrl().get_dealer_id()
    dealer_index = 0
    start_urls = [base_url % dealer_list[dealer_index]]

    def parse(self, response):
        item = DealerSpecScrapyItem()
        yield Request(response.url, callback=self.parse_series_item, meta={'item': copy.deepcopy(item)},
                      dont_filter=True)

    def parse_series_item(self, response):
        item = response.meta['item']
        content = json.loads(response.body.decode())
        for element in content:
            series_list = element["SeriesList"]
            for series in series_list:
                item["dealer_id"] = self.dealer_list[self.dealer_index]
                item["series_id"] = series["SeriesId"]
                item["series_vr_url"] = str(series["SeriesVRUrl"])
                url = self.spec_base_url % (item["dealer_id"], item["series_id"])
                yield Request(url, callback=self.parse_spec_item, meta={'item': copy.deepcopy(item)}, dont_filter=True)
        self.dealer_index += 1
        if self.dealer_list[self.dealer_index] < len(self.dealer_list):
            url = self.base_url % (self.dealer_list[self.dealer_index])
            yield Request(url=url, callback=self.parse_series_item, meta={"item": copy.deepcopy(item)},
                          dont_filter=True)

    def parse_spec_item(self, response):
        item = response.meta['item']
        content = json.loads(response.body.decode())
        for element in content:
            s_list = element["slist"]
            for spec in s_list:
                item["spec_id"] = spec["SpecId"]
                item["price"] = spec["Price"]
                item["time"] = get_current_date()
                yield item
