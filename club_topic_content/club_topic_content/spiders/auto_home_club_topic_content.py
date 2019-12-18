# -*- coding: utf-8 -*-
import re

import scrapy
from bs4 import BeautifulSoup
from club_topic_content.items import ClubTopicContentItem
from lib.translate import get_rule
from models.club import StructureStartUrl


class AutoHomeClubTopicContentSpider(scrapy.Spider):
    name = 'auto_home_club_topic_content'

    def __init__(self):
        self.index = 1
        self.base_url = "https://forum.app.autohome.com.cn/forum_v7.9.5/forum/club/topiccontent-a2-pm2-v8.8.0-t%s-o0-p1-s20-c1-nt0-fs0-sp0-al0-cw360-i0-ct1.json"
        self.topic_list = StructureStartUrl().get_topic_id()

    def start_requests(self):

        for i in self.topic_list:
            start_url = self.base_url % i
            yield scrapy.Request(url=start_url, callback=self.parse, meta={"topic_id": i})

    def parse(self, response):
        item = ClubTopicContentItem()
        soup = BeautifulSoup(response.body.decode('utf-8'))
        rule = get_rule(response.text)
        soup_node_list = soup.find('div', {'class': 'host-content'})
        span_list = soup_node_list.contents[0].find_all('span')
        for span in span_list:
            try:
                span.append(rule[span["class"][0]])
            except:
                pass
        item["content"] = soup_node_list.get_text().split('(function')[0].strip()
        item["topic_id"] = response.meta["topic_id"]
        yield item