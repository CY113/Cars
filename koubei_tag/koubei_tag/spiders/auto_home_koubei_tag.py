# -*- coding: utf-8 -*-
import json
import scrapy
from koubei_tag.items import KoubeiTagItem
from models.koubei import StructureStartUrl


class AutoHomeKoubeiTagSpider(scrapy.Spider):
    name = 'auto_home_koubei_tag'
    series_list = StructureStartUrl().get_series_id()
    base_url = "https://koubei.app.autohome.com.cn/autov8.6.5/alibi/seriesalibiinfos-pm2-ss%s-st0-p1-s20-isstruct1-o0.json"
    series_index = 0
    start_urls = [base_url % series_list[series_index][0]]

    def parse(self, response):
        item = KoubeiTagItem()
        content = json.loads(response.body.decode(), strict=False)
        result = content["result"]
        if len(result["structuredlist"]) > 0:
            for structure in result["structuredlist"]:
                item["series_id"] = self.series_list[self.series_index][0]
                item["tag_id"] = structure["id"]
                for summary in structure["Summary"]:
                    if summary["SummaryKey"] != 0:
                        item["combination"] = summary["Combination"]
                        item["summary_key"] = summary["SummaryKey"]
                        yield item

        self.series_index += 1
        if self.series_index < len(self.series_list):
            url = self.base_url % self.series_list[self.series_index][0]
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
