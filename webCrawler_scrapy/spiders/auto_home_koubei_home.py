# -*- coding: utf-8 -*-

import json
import copy
from scrapy import Spider
from scrapy import Request
from item.koubei_home_items import KoubeiHomeItem
from models.koubei import StructureStartUrl


class KoubeiHomeSpider(Spider):
    name = "koubei_home"
    base_url = "https://koubei.app.autohome.com.cn/autov8.6.5/alibi/NewEvaluationInfo.ashx?eid=%s&useCache=1"
    series_id_list = StructureStartUrl().get_home_koubei_id()
    # series_id_list = [(94353,)]
    series_index = 0
    start_urls = [base_url % series_id_list[series_index][0]]

    # 解析口碑分页
    def parse(self, response):
        item = KoubeiHomeItem()
        try:
            content = json.loads(response.body.decode())
            result = content["result"]
            item["koubei_id"] = self.series_id_list[self.series_index][0]
            item["pid"] = result["boughtprovince"]
            item["cid"] = result["boughtcity"]
            item["dealer_id"] = result["dealer"]
            yield item
            self.series_index += 1
            if self.series_index < len(self.series_id_list):
                url = self.base_url % (self.series_id_list[self.series_index][0])
                yield Request(url=url, callback=self.parse, meta={'item': copy.deepcopy(item)}, dont_filter=True)
        except Exception as e:
            print(self.series_id_list[self.series_index][0])
            yield
