# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from club_topic_comments.items import ClubTopicCommentsItem
from lib.translate import get_rule
from models.club import StructureStartUrl


class AutoHomeClubTopicCommentsSpider(scrapy.Spider):
    name = 'auto_home_club_topic_comments'
    club_index = 0
    page_index = 1

    club_id_list = StructureStartUrl().get_topic_id()
    base_url = "https://forum.app.autohome.com.cn/forum_v7.9.5/forum/club/topiccontent-a2-pm2-v8.8.0-t%s-o0-p%s-s20-c1-nt0-fs0-sp0-al0-cw360-i0-ct1.json"
    start_urls = [base_url % (club_id_list[club_index], page_index)]

    def parse(self, response):
        item = ClubTopicCommentsItem()
        i = 0
        soup = BeautifulSoup(response.body.decode('utf-8'))
        node_list = response.xpath("//*[@class=\"post-flow\"]/li")

        soup_node_list = soup.find_all('div', {'class': 'user-content'})
        for node in node_list:
            rule = get_rule(response.text)
            item["topic_id"] = self.club_id_list[self.club_index]
            try:
                item["user"] = node.xpath(
                    ".//span[@class=\"name\"]/a/text()").extract()[0]
            except Exception as e:
                item["user"] = ""
            try:
                item["user_id"] = node.xpath(
                    './/span[@class="name"]/a/@href').get().split("㊣")[1]
            except Exception as e:
                item["user_id"] = ""
            try:
                span_list = soup_node_list[i].find_all('span')
                for span in span_list:
                    span.append(rule[span["class"][0]])
                item["content"] = soup_node_list[i].get_text().strip("\n")
            except Exception as e:
                item["content"] = "该帖已删除"
            try:
                item["publish_time"] = node.xpath(
                    './/*[@class="time"]/text()').extract()[0]
            except Exception as e:
                item["publish_time"] = ""
            try:
                item["id"] = node.xpath(
                    './/span[@class="flowLevel"]/span/text()').extract()[0]
            except Exception as e:
                item["id"] = ""
            if item["id"] != "":
                yield item
                i += 1
        self.page_index += 1
        if 0 < len(soup_node_list) <= 20:
            url = self.base_url % (
                self.club_id_list[self.club_index], self.page_index)
            yield scrapy.Request(url=url, callback=self.parse)
        else:
            self.club_index += 1
            if self.club_index < len(self.club_id_list):
                self.page_index = 1
                url = self.base_url % (
                    self.club_id_list[self.club_index], self.page_index)
                yield scrapy.Request(url=url, callback=self.parse)

