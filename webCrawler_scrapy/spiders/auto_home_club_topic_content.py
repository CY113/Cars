# -*- coding: utf-8 -*-

import re
import copy
import requests
from lxml import html
from scrapy import Request
from scrapy.spiders import Spider
from item.club_topic_content_items import ClubTopicContentItem
from fontTools.ttLib import TTFont


class AutoHomeTopicContentSpider(Spider):
    name = "club_topic_content"
    club_list = [(2778, 69436529)]
    base_url = "https://club.autohome.com.cn/bbs/thread-c-%s-%s-1.html"
    start_urls = [base_url % (club_list[0][0], club_list[0][1])]

    def parse(self, response):
        item = ClubTopicContentItem()
        text = response.body.decode('gb2312')
        response = html.fromstring(text)
        # 匹配ttf font
        cmp = re.compile(",url\('(//.*.ttf)'\) format\('woff'\)")
        rst = cmp.findall(text)
        ttf = requests.get("http:" + rst[0], stream=True)
        with open("autohome.ttf", "wb") as pdf:
            for chunk in ttf.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)
        # 解析字体库font文件
        font = TTFont('autohome.ttf')
        uniList = font['cmap'].tables[0].ttFont.getGlyphOrder()
        utf8List = [eval("'\\u" + uni[3:] + "'").encode('utf-8') for uni in uniList[1:]]

        wordList = ['一', '七', '三', '上', '下', '不', '中', '档', '比', '油', '泥', '灯', '九', '了', '二', '五', '低', '保', '光', '八',
                    '公', '六', '养', '内', '冷', '副', '加', '动', '十', '电', '的', '皮', '盘', '真', '着', '路', '身', '软', '过', '近',
                    '远', '里', '量', '长', '门', '问', '只', '右', '启', '呢', '味', '和', '响', '四', '地', '坏', '坐', '外', '多', '大',
                    '好', '孩', '实', '小', '少', '短', '矮', '硬', '空', '级', '耗', '雨', '音', '高', '左', '开', '当', '很', '得', '性',
                    '自', '手', '排', '控', '无', '是', '更', '有', '机', '来']
        # 获取发帖内容
        note = response.cssselect(".tz-paragraph")[0].text_content().encode('utf-8')
        for i in range(len(utf8List)):
            note = note.replace(utf8List[i], wordList[i].encode('utf-8'))
        item["content"] = note.decode()
        yield item
