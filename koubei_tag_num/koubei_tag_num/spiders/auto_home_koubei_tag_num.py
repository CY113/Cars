# -*- coding: utf-8 -*-
import json
import scrapy
from koubei_tag_num.items import KoubeiTagNumItem
from lib.GetCurrentTime import get_current_date
from models.koubei import StructureStartUrl


class AutoHomeKoubeiTagNumSpider(scrapy.Spider):
    name = 'auto_home_koubei_tag_num'
    series_list = StructureStartUrl().get_series_id()  # 获取在售车系的口碑数据
    series_index = 0
    base_url = "https://koubei.app.autohome.com.cn/autov8.6.5/alibi/seriesalibiinfos-pm2-ss%s-st0-p1-s20-isstruct1-o0.json"
    start_urls = [base_url % series_list[series_index][0]]

    def parse(self, response):
        item = KoubeiTagNumItem()
        content = json.loads(response.body.decode())
        result = content["result"]
        if len(result["structuredlist"]) > 0:
            structure = result["structuredlist"][0]
            for summary in structure["Summary"]:
                if summary["SummaryKey"] != 0:
                    item["summary_key"] = summary["SummaryKey"]
                    item["volume"] = summary["Volume"]
                    item["time"] = get_current_date()
                    yield item

        # 翻页操作
        self.series_index += 1
        if self.series_index < len(self.series_list):
            url = self.base_url % self.series_list[self.series_index][0]
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
