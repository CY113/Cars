# -*- coding: utf-8 -*-
import json
import scrapy
from koubei_read.items import KoubeiReadItem
from lib.GetCurrentTime import get_current_date
from models.koubei import StructureStartUrl


class AutoHomeKoubeiReadSpider(scrapy.Spider):
    name = 'auto_home_koubei_read'
    koubei_list = StructureStartUrl().get_koubei_id()
    koubei_index = 0
    base_url = "https://koubei.app.autohome.com.cn/autov8.6.5/alibi/NewEvaluationInfo.ashx?eid=%s&useCache=1"
    start_urls = [base_url % (koubei_list[koubei_index])]

    def parse(self, response):
        item = KoubeiReadItem()
        content = json.loads(response.body.decode())
        item["koubei_id"] = content["result"]["eid"]
        node = content["result"]
        item["visit_count"] = node["visitcount"]
        item["helpful_count"] = node["helpfulcount"]
        item["comment_count"] = node["commentcount"]
        item["time"] = get_current_date()
        yield item

        self.koubei_index += 1
        if self.koubei_index < len(self.koubei_list):
            url = self.base_url % (self.koubei_list[self.koubei_index])
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
