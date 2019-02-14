# -*- coding: utf-8 -*-

import math
import copy
from scrapy import Request
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider
from models.club import StructureStartUrl
from item.club_topic_comment_items import ClubTopicCommentScrapyItem


class AutoHomeTopicCommentSpider(CrawlSpider):
    name = "club_topic_comment"
    offset = 0
    club_index = 0
    page_index = 1
    # club_id_list = StructureStartUrl().get_topic_id(offset)
    club_id_list = [5411619]

    base_url = "https://forum.app.autohome.com.cn/forum_v7.9.5/forum/club/topiccontent-a2-pm2-v8.8.0-t%s-o0-p%s-s20-c1-nt0-fs0-sp0-al0-cw360-i0-ct1.json"
    start_urls = [base_url % (club_id_list[club_index], page_index)]

    def parse(self, response):
        item = ClubTopicCommentScrapyItem()
        yield Request(url=response.url, callback=self.parse_club_topic_comment_items,
                      meta={"item": copy.deepcopy(item)})

    def parse_club_topic_comment_items(self, response):
        i = 0
        item = response.meta['item']
        soup = BeautifulSoup(response.body.decode())
        node_list = response.xpath("//*[@class=\"post-flow\"]/li")
        soup_node_list = soup.find_all('div', {'class': 'user-content'})
        for node in node_list:
            item["topic_id"] = self.club_id_list[self.club_index]
            try:
                item["user"] = node.xpath(".//span[@class=\"name\"]/a/text()").extract()[0]
            except Exception as e:
                item["user"] = ""
            try:
                item["content"] = soup_node_list[i].get_text().strip("\n")
            except Exception as e:
                item["content"] = ""
            try:
                item["publish_time"] = node.xpath('.//*[@class="time"]/text()').extract()[0]
            except Exception as e:
                item["publish_time"] = ""
            try:
                item["id"] = node.xpath('.//span[@class="flowLevel"]/span/text()').extract()[0]
            except Exception as e:
                item["id"] = ""
            if item["id"] != "":
                yield item
                i += 1

        self.page_index += 1
        if 0 < len(soup_node_list) <= 20:
            url = self.base_url % (self.club_id_list[self.club_index], self.page_index)
            yield Request(url=url, callback=self.parse_club_topic_comment_items, meta={"item": copy.deepcopy(item)})
        else:
            self.club_index += 1
            if self.club_index < len(self.club_id_list):
                self.page_index = 1
                url = self.base_url % (self.club_id_list[self.club_index], self.page_index)
                yield Request(url=url, callback=self.parse_club_topic_comment_items, meta={"item": copy.deepcopy(item)})
            else:
                self.offset += 1000
                self.club_id_list = StructureStartUrl().get_topic_id(self.offset)
                if 1000 >= len(self.club_id_list) > 0:
                    self.club_index = 0
                    self.page_index = 1
                    url = self.base_url % (self.club_id_list[self.club_index], self.page_index)
                    yield Request(url=url, callback=self.parse_club_topic_comment_items,
                                  meta={"item": copy.deepcopy(item)})
