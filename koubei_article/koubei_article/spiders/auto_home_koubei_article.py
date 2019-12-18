# -*- coding: utf-8 -*-
import json
import re

import scrapy
from koubei_article.items import KoubeiArticleItem
from lib.GetCurrentTime import get_current_date
from models.koubei import StructureStartUrl


class AutoHomeKoubeiArticleSpider(scrapy.Spider):
    name = 'auto_home_koubei_article'
    koubei_list = StructureStartUrl().get_koubei_id()
    koubei_index = 0
    base_url = "https://koubei.app.autohome.com.cn/autov8.6.5/alibi/NewEvaluationInfo.ashx?eid=%s&useCache=1"
    start_urls = [base_url % koubei_list[koubei_index]]

    def parse(self, response):
        item = KoubeiArticleItem()
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
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
