# -*- coding: utf-8 -*-
import scrapy

from models.article import StructureArticleID


class AutoHomeArticleContentSpider(scrapy.Spider):
    name = 'auto_home_article_content'
    article_id_list = StructureArticleID().get_article_id()
    article_id_index = 0
    base_url = "https://cont.app.autohome.com.cn/cont_v8.5.0/content/news/newscontent-pm2-n%s-t0-rct1-ish0-ver%s.json"
    start_urls = [base_url % (article_id_list[article_id_index][0], article_id_list[article_id_index][1])]

    def parse(self, response):
        item = ArticleContentScrapyItem()
        yield Request(url=response.url, callback=self.parse_article_content_items, meta={"item": copy.deepcopy(item)}, dont_filter=True)

    def parse_article_content_items(self, response):
        item = response.meta['item']
        item["id"] = self.article_id_list[self.article_id_index][0]
        item["content"] = extract_article(response.url)
        yield item
        self.article_id_index += 1
        if self.article_id_index < len(self.article_id_list):
            url = self.base_url % (self.article_id_list[self.article_id_index][0], self.article_id_list[self.article_id_index][1])
            yield Request(url=url, callback=self.parse_article_content_items, meta={"item": copy.deepcopy(item)},
                          dont_filter=True)
