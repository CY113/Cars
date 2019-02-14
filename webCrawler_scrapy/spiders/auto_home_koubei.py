# -*- coding: utf-8 -*-

import json
import copy
import scrapy
from item.koubei_items import KoubeiScrapyItem
from scrapy import Request
from models.koubei import StructureStartUrl


class AutoHomeKoubeiSpider(scrapy.spiders.Spider):
    name = "koubei"
    base_url = "https://koubei.app.autohome.com.cn/autov9.1.0/alibi/seriesalibiinfos-pm2-ss%s-st0-p%s-s20-isstruct0-o0.json"
    series_id_list = StructureStartUrl().get_series_id()
    # series_id_list = [(145,)]
    page_index = 1
    url_index = 0
    start_urls = [base_url % (series_id_list[url_index][0], page_index)]

    # 解析口碑分页
    def parse(self, response):
        item = KoubeiScrapyItem()
        yield Request(url=response.url, callback=self.parse_koubei_item, meta={'item': copy.deepcopy(item)},
                      dont_filter=True)

    # 解析口碑排行内容
    def parse_koubei_item(self, response):
        item = response.meta['item']
        content = json.loads(response.body.decode())
        result = content["result"]
        # content_base_url = "https://koubei.app.autohome.com.cn/autov8.6.5/alibi/NewEvaluationInfo.ashx?eid=%s&useCache=1"
        if len(result["list"]) > 0:
            for koubei in result["list"]:
                item["koubei_id"] = koubei["Koubeiid"]
                item["spec_id"] = koubei["specid"]
                item["user_id"] = koubei["userid"]
                item["buy_price"] = koubei["buyprice"].rstrip("万")
                item["post_time"] = koubei["posttime"]
                item["page_num"] = content["result"]["pagecount"]
                yield item
                # detail_url = content_base_url % koubei["Koubeiid"]
                # yield Request(url=detail_url, callback=self.parse_koubei_details_item,
                #               meta={'item': copy.deepcopy(item)}, dont_filter=True)
        else:
            item["page_num"] = 0
        self.page_index += 1
        if self.page_index <= item["page_num"]:
            url = self.base_url % (self.series_id_list[self.url_index][0], self.page_index)
            yield Request(url=url, callback=self.parse_koubei_item, meta={'item': copy.deepcopy(item)},
                          dont_filter=True)
        else:
            self.url_index += 1
            if self.url_index < len(self.series_id_list):
                self.page_index = 1
                url = self.base_url % (self.series_id_list[self.url_index][0], self.page_index)
                yield Request(url=url, callback=self.parse_koubei_item, meta={'item': copy.deepcopy(item)},
                              dont_filter=True)
    #
    # # 解析口碑内容
    # def parse_koubei_details_item(self, response):
    #     try:
    #         content = json.loads(response.body.decode())
    #         item = response.meta['item']
    #         result = content["result"]
    #         item["pid"] = result["boughtprovince"]
    #         item["cid"] = result["boughtcity"]
    #         item["dealer_id"] = result["dealer"]
    #         yield item
    #     except Exception as e:
    #         print(json.loads(response.body.decode()))
    #         item["pid"] = result["boughtprovince"]
    #         item["cid"] = result["boughtcity"]
    #         item["dealer_id"] = result["dealer"]
    #         yield item
