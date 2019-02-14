# -*- coding: utf-8 -*-

import json

import scrapy
import time
from scrapy import Request
from item.koubei_rank_items import KoubeiRankScrapyItem
from models.koubei import StructureStartUrl
from lib.GetCurrentTime import get_current_date


class AutoHomeKoubeiRankSpider(scrapy.spiders.Spider):
    name = "koubei_rank"
    base_url = "https://koubei.app.autohome.com.cn/autov8.8.5/alibi/alibiseriesrank-pm2-categoryid%s-struct0-order0-price0.json"
    level_list = StructureStartUrl().get_level_id()
    url_index = 0
    start_urls = [base_url % url_index]

    def parse(self, response):
        result = json.loads(response.body.decode())["result"]
        item = KoubeiRankScrapyItem()
        for series in result["serieslist"]:
            item["level_id"] = result["categoryid"]
            item["series_id"] = series["seriesid"]
            item["koubei_rank"] = series["rank"]
            item["koubei_score"] = series["score"]
            item["koubei_evaluation_count"] = series["evaluationcount"]
            item["koubei_update_time"] = get_current_date()
            yield item
            time.sleep(1)
        self.url_index += 1
        if self.url_index < len(self.level_list):
            url = self.base_url % self.level_list[self.url_index]
            yield Request(url=url, callback=self.parse)


