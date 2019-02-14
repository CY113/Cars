# -*- coding: utf-8 -*-

import re
import copy
import json
import scrapy
from item.dealer_items import DealerScrapyItem
from lib.GetCurrentTime import get_current_date
from scrapy import Request


class AutoHomeDealerSpider(scrapy.spiders.Spider):
    name = "dealer"

    start_urls = ["https://dealer.autohome.com.cn/Ajax?actionName=GetAreasAjax&ajaxProvinceId=0"]

    def parse(self, response):
        item = DealerScrapyItem()
        base_url = "https://dealer.autohome.com.cn/"
        area_info_groups = json.loads(str(response.body, encoding='gbk'))["AreaInfoGroups"]  # 二进制转字符串,转成GBK编码
        for area in area_info_groups:
            for value in area["Values"]:
                item["dealer_city"] = value["Pinyin"]
                url = base_url + value["Pinyin"]
                yield Request(url, callback=self.parse_pagination_item, meta={'item': copy.deepcopy(item)},
                              dont_filter=True)

    def parse_pagination_item(self, response):
        item = response.meta['item']
        base_url = "https://dealer.autohome.com.cn/%s?countyId=0&brandId=0&seriesId=0&factoryId=0&pageIndex=%s&kindId=1&orderType=0&isSales=0"
        dealer_count = re.search(r"dealerCount\s*=\s*\d+", response.text).group().strip("dealerCount = ")
        if dealer_count != 0:
            for pageIndex in range(1, int(dealer_count) + 1):
                url = base_url % (item["dealer_city"], pageIndex)
                yield Request(url, callback=self.parse_item, meta={'item': copy.deepcopy(item)}, dont_filter=True)

    def parse_item(self, response):
        base_url = "https://dealerframe.m.autohome.com.cn/dealerm/ajax/GetDealerInfo?dealerId=%s"
        selector = scrapy.Selector(response)
        item = response.meta['item']
        dealer_urls = selector.xpath("//li[@class=\"list-item\"]/a/@href").extract()
        for dealer_url in dealer_urls:
            item["dealer_id"] = re.search("/\d+/", dealer_url).group().strip("/")
            url = base_url % (item["dealer_id"])
            yield Request(url, callback=self.parse_dealer, meta={'item': copy.deepcopy(item)}, dont_filter=True)

    def parse_dealer(self, response):
        content = json.loads(response.body.decode())
        item = response.meta['item']
        item["company"] = content["Company"]
        item["company_simple"] = content["CompanySimple"]
        item["address"] = content["Address"]
        item["pid"] = content["PID"]
        item["cid"] = content["CID"]
        item["sid"] = content["SID"]
        item["business_area"] = content["OrderRangeTitle"]
        item["lon"] = content["MapLonBaidu"]
        item["lat"] = content["MapLatBaidu"]
        item["kind_id"] = content["KindID"]
        item["star_level"] = content["StarLevel"]
        item["update_time"] = get_current_date()
        return item
