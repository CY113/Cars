# -*- coding: utf-8 -*-

import copy
import json
import re
from scrapy import Request
from scrapy.spiders import CrawlSpider
from lib.util import check_json_format
from item.user_items import UserScrapyItem


class AutoHomeUsersSpider(CrawlSpider):
    name = "users"
    start_urls = ["http://mobile.app.autohome.com.cn/user_v7.0.0/User/GetUserInfo.ashx?tid=11967537"]
    user_id = 11967537

    def parse(self, response):
        item = UserScrapyItem()
        yield Request(url=response.url, callback=self.parse_user_items, meta={"item": copy.deepcopy(item)})

    def parse_user_items(self, response):
        self.user_id += 1
        item = response.meta['item']
        content = response.body.decode()
        if check_json_format(content):
            content = json.loads(content)
        else:
            content = re.sub('"title":".{6,30}",', '"title":" ",', content)
            content = json.loads(content)
        if "无结果集" not in content["message"] or "GetInfoFromUserCenter(int userId) is null" not in content[
            "message"]:
            result = content["result"]
            item["user_id"] = result["userid"]
            item["user_name"] = result["name"]
            item["user_sex"] = result["sex"]
            item["user_regtime"] = result["regtime"]
            item["user_pid"] = result["provinceid"]
            item["user_cid"] = result["cityid"]
            yield item
        if self.user_id <= 100000000:
            base_url = "http://mobile.app.autohome.com.cn/user_v7.0.0/User/GetUserInfo.ashx?tid=%s"
            url = base_url % self.user_id
            yield Request(url=url, callback=self.parse_user_items, meta={"item": copy.deepcopy(item)})
