# -*- coding: utf-8 -*-
import json
import time
import scrapy
from koubei_rank.items import KoubeiRankItem
from lib.GetCurrentTime import get_current_date
from models.koubei import StructureStartUrl


class AutoHomeKoubeiRankSpider(scrapy.Spider):
    name = 'auto_home_koubei_rank'
    base_url = "https://koubei.app.autohome.com.cn/autov8.8.5/alibi/alibiseriesrank-pm2-categoryid%s-struct0-order0-price0.json"
    level_list = StructureStartUrl().get_level_id()
    url_index = 0
    start_urls = [base_url % url_index]

    def parse(self, response):
        item = KoubeiRankItem()
        result = json.loads(response.body.decode())["result"]
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
            yield scrapy.Request(url=url, callback=self.parse)
