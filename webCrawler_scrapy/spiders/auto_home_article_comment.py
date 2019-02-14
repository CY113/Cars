# -*- coding: utf-8 -*-

import copy
import json
import math
from scrapy import Request
from scrapy.spiders import CrawlSpider
from models.article import StructureArticleID
from lib.GetCurrentTime import get_current_date
from item.article_comment_items import ArticleCommentScrapyItem


class AutoHomeArticleCommentSpider(CrawlSpider):
    name = "article_comment"
    article_list = StructureArticleID().get_article_id()
    article_index = 0
    page_index = 1
    last_time = 0
    base_url = "https://newsnc.app.autohome.com.cn/reply_v7.9.0/news/comments-pm2-n%s-o0-s20-lastid%s-t0.json"
    start_urls = [base_url % (article_list[article_index][0], last_time)]

    def parse(self, response):
        item = ArticleCommentScrapyItem()
        print(response.url)
        yield Request(url=response.url, callback=self.parse_article_comment_items, meta={"item": copy.deepcopy(item)},
                      dont_filter=True)

    def parse_article_comment_items(self, response):
        item = response.meta['item']
        content = json.loads(response.body.decode(), strict=False)
        comment_list = content["result"]["list"]
        for comment in comment_list:
            item["article_id"] = self.article_list[self.article_index][0]
            item["comment_id"] = comment["id"]
            item["floor"] = comment["floor"]
            item["user_id"] = comment["nameid"]
            item["publish_time"] = comment["time"]
            item["content"] = comment["content"]
            item["update_time"] = get_current_date()
            yield item
        self.last_time = item["comment_id"]
        self.page_index += 1
        if math.ceil(content["result"]["totalcount"] / 20) >= self.page_index:
            url = self.base_url % (self.article_list[self.article_index][0], self.last_time)
            yield Request(url=url, callback=self.parse_article_comment_items, meta={"item": copy.deepcopy(item)},
                          dont_filter=True)
        else:
            self.article_index += 1
            if self.article_index < len(self.article_list):
                self.page_index = 1
                self.last_time = 0
                url = self.base_url % (self.article_list[self.article_index][0], self.last_time)
                print(url)
                yield Request(url=url, callback=self.parse_article_comment_items, meta={"item": copy.deepcopy(item)},
                              dont_filter=True)
