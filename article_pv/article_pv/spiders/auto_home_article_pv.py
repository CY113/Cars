# -*- coding: utf-8 -*-
import json
import re

import scrapy

from article_pv.items import ArticlePvItem
from lib.GetCurrentTime import get_current_date
from models.article import StructureArticleID


class AutoHomeArticlePvSpider(scrapy.Spider):
    name = 'auto_home_article_pv'
    article_list = StructureArticleID().get_article_id()
    article_index = 0
    base_url = "https://cont.app.autohome.com.cn/cont_v8.5.0/cont/articlepv?callback=updateArticlePV&pm=1&ids=%s"
    start_urls = [base_url % (article_list[article_index][0])]

    def parse(self, response):
        item = ArticlePvItem()
        content = re.search(r"{[^}]+}][^}]+}", response.body.decode()).group()
        content = json.loads(content, strict=False)
        result = content["result"][0]
        item["article_id"] = result["id"]
        item["pv_count"] = result["pvcount"]
        item["update_time"] = get_current_date()
        yield item
        self.article_index += 1
        if len(self.article_list) > self.article_index:
            url = self.base_url % (self.article_list[self.article_index][0])
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
