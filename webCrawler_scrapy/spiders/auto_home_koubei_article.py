# -*- coding: utf-8 -*-

import re
import json
import copy
import time
import scrapy
from scrapy import Request
from models.koubei import StructureStartUrl
from lib.GetCurrentTime import get_current_date
from item.koubei_koubei_article_items import KoubeiArticleScrapyItem


class AutoHomeKoubeiArticleSpider(scrapy.spiders.Spider):
    name = "koubei_article"
    koubei_list = StructureStartUrl().get_koubei_id()
    koubei_index = 0
    base_url = "https://koubei.app.autohome.com.cn/autov8.6.5/alibi/NewEvaluationInfo.ashx?eid=%s&useCache=1"
    start_urls = [base_url % koubei_list[koubei_index]]

    def parse(self, response):
        item = KoubeiArticleScrapyItem()
        yield Request(url=response.url, callback=self.parse_koubei_article_item, meta={"item": copy.deepcopy(item)},
                      dont_filter=True)

    # 解析口碑详情字段
    def parse_koubei_article_item(self, response):
        item = response.meta['item']
        content = json.loads(response.body.decode())
        item["koubei_id"] = content["result"]["eid"]
        node_value = content["result"]
        for node in node_value:
            if re.search(r"[a-zA-Z]+Scene", node):
                item["feeling_name"] = node_value[node]["feelingname"]
                item["feeling"] = node_value[node]["feeling"]
                item["score"] = node_value[node]["score"]
                item["time"] = get_current_date()
                yield item

        # 翻页操作
        self.koubei_index += 1
        if self.koubei_index < len(self.koubei_list):
            url = self.base_url % (self.koubei_list[self.koubei_index])
            yield Request(url=url, callback=self.parse_koubei_article_item, meta={"item": copy.deepcopy(item)},
                          dont_filter=True)
