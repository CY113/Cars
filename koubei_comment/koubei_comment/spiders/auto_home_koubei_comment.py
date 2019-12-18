# -*- coding: utf-8 -*-
import json

import scrapy
from koubei_comment.items import KoubeiCommentItem
from lib.GetCurrentTime import get_current_date
from lib.formmat_time import formmat_time
from models.koubei import StructureStartUrl


class AutoHomeKoubeiCommentSpider(scrapy.Spider):
    name = 'auto_home_koubei_comment'
    base_url = "https://koubei.app.autohome.com.cn/autov8.6.5/news/koubeicomments-pm2-n%s-s20-lastid%s.json"
    comment_list = StructureStartUrl().get_koubei_id()
    comment_index = 0
    last_id = 0
    comment_id_list = []
    start_urls = [base_url % (comment_list[comment_index], last_id)]

    def parse(self, response):
        item = KoubeiCommentItem()
        content = json.loads(response.body.decode())
        result = content["result"]
        item["koubei_id"] = self.comment_list[self.comment_index]
        if len(result["list"]) > 0:
            for comment_list in result["list"]:
                item["id"] = comment_list["id"]
                item["user_id"] = comment_list["nameid"]
                item["content"] = comment_list["content"]
                item["carname"] = comment_list["carname"]
                create_time = comment_list["time"]
                if "前" in create_time:
                    item["create_time"] = formmat_time(create_time)
                else:
                    item["create_time"] = comment_list["time"]
                item["time"] = get_current_date()
                self.comment_id_list.append(str(comment_list["id"]))
                yield item
        if len(result["list"]) == 20 and (result["pageid"] == self.comment_id_list[-1]):
            url = self.base_url % (self.comment_list[self.comment_index], self.comment_id_list[-1])
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
        else:
            self.comment_index += 1
            if self.comment_index < len(self.comment_list):
                self.last_id = 0
                url = self.base_url % (self.comment_list[self.comment_index], self.last_id)
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
