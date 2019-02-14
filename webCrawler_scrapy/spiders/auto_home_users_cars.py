# -*- coding: utf-8 -*-
import re
import copy
import json
from scrapy import Request
from item.user_cars_items import UserCarsScrapyItem
from lib.GetCurrentTime import get_current_date,timestamp_to_localtime
from scrapy.spiders import CrawlSpider


class AutoHomeUserCarsSpider(CrawlSpider):
    name = "user_cars"
    start_urls = ["https://i.autohome.com.cn/ajax/home/OtherHomeAppsData?appname=Car&TuserId=1357363"]

    def parse(self, response):
        item = UserCarsScrapyItem()
        item["user_id"] = re.search("\d+", response.url).group()
        yield Request(url=response.url, callback=self.parse_user_cars_item, meta={"item": copy.deepcopy(item)})

    def parse_user_cars_item(self, response):
        item = response.meta["item"]
        content = json.loads(response.body.decode('gbk'))
        concern_info_list = content["ConcernInfoList"]
        for concern in concern_info_list:
            item["spec_id"] = concern["SpecId"]
            item["cert_date"] = timestamp_to_localtime(int(concern["datetime"].rstrip("/)").lstrip("/Date(")))
            item["time"] = get_current_date()
            yield item
