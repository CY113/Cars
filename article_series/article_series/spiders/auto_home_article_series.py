# -*- coding: utf-8 -*-
import scrapy
import re
import json
from urllib import parse
from article_series.items import ArticleSeriesItem
from models.article import StructureArticleID


class AutoHomeArticleSeriesSpider(scrapy.Spider):
    name = 'auto_home_article_series'
    base_url = "https://cont.app.autohome.com.cn/cont_v9.2.5/content/news/newscontent-pm2-n%s-t0-rct0-ver%s.json"
    article_list = StructureArticleID().get_article_id()
    article_index = 0
    start_urls = [base_url % article_list[article_index]]

    def parse(self, response):
        item = ArticleSeriesItem()
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
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
