# -*- coding: utf-8 -*-

import re
import json
from urllib import parse
from scrapy import Request, Spider
from item.article_series_items import ArticleSeriesItems
from models.article import StructureArticleID


class ArticleSeriesSpider(Spider):
    name = 'article_series'
    base_url = "https://cont.app.autohome.com.cn/cont_v9.2.5/content/news/newscontent-pm2-n%s-t0-rct0-ver%s.json"
    # article_list = [(916149, 20180423170139), (914645, 20180423184913), (914664, 20180423184954)]  #
    article_list = StructureArticleID().get_article_id()
    article_index = 0
    start_urls = [base_url % article_list[article_index]]

    def parse(self, response):
        item = ArticleSeriesItems()
        try:
            set_value = re.search('setValue\(".+"\)', response.body.decode()).group()
        except Exception as e:
            set_value = ""
        if set_value != "":
            set_value = set_value.lstrip('setValue("').rstrip('")')
            unquote_set_value = parse.unquote(set_value)
            series_list = json.loads(unquote_set_value)["serieslist"]
            if len(series_list) > 0:
                for series in series_list:
                    item["id"] = self.article_list[self.article_index][0]  # 文章ID
                    item["series_id"] = series['seriesid']  # 文章相关车系id
                    yield item

        self.article_index += 1

        if self.article_index < len(self.article_list):  # 进行翻页
            url = self.base_url % self.article_list[self.article_index]
            yield Request(url=url, callback=self.parse, dont_filter=True)
