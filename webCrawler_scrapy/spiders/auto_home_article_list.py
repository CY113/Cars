# -*- coding: utf-8 -*-


import copy
import json
from scrapy import Request
from scrapy.spiders import CrawlSpider
from lib.GetCurrentTime import get_current_date
from item.article_list_items import ArticleListScrapyItem


class AutoHomeArticleListSpider(CrawlSpider):
    name = "article_list"
    last_time = 0
    type_index = 0
    type_list = [1, 3, 60, 82, 102, 97, 97107]
    base_url = "https://newsnc.app.autohome.com.cn/news_v9.2.5/news/orinews-pm2-l%s-s30-focus0-v9.2.5-t%s-cid110100.json"
    start_urls = [base_url % (last_time, type_list[type_index])]

    def parse(self, response):
        item = ArticleListScrapyItem()
        yield Request(url=response.url, callback=self.parse_article_list_items, meta={"item": copy.deepcopy(item)},
                      dont_filter=True)

    def parse_article_list_items(self, response):
        item = response.meta['item']
        content = json.loads(response.body.decode(), strict=False)
        news_list = content["result"]["newslist"]
        item["last_time"] = content["result"]["pageid"]
        for news in news_list:
            news = news["data"]
            item["id"] = news["id"]
            item["title"] = news["title"]
            item["media_type"] = news["mediatype"]
            item["type"] = news["type"]
            item["publish_time"] = news["updatetime"]
            item["author"] = news["thirdsource"]
            try:
                item["ver"] = news["ver"]
            except Exception as e:
                item["ver"] = ""
            item["update_time"] = get_current_date()

            yield item
        self.last_time = item["last_time"]
        if len(news_list) == 30:
            url = self.base_url % (self.last_time, self.type_list[self.type_index])
            yield Request(url=url, callback=self.parse_article_list_items, meta={"item": copy.deepcopy(item)},
                          dont_filter=True)
        else:
            self.type_index += 1
            if self.type_index < len(self.type_list):
                self.last_time = 0
                url = self.base_url % (self.last_time, self.type_list[self.type_index])
                yield Request(url=url, callback=self.parse_article_list_items, meta={"item": copy.deepcopy(item)},
                              dont_filter=True)
