#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: whb
@license: Apache Licence  
@contact: 1223934389@qq.com 
@software: PyCharm 
@file: qunar.py 
@time: 18-11-19 下午1:49 
"""

from scrapy import Selector, Request
from ..utils import parse_data_kit
import time
import scrapy.http.response
import re
from ..items import QunarAreaListItem, QunarPoiListItem, UrlItem
from ..utils.database_kit import Redis


class QunarAreaListSpider(scrapy.Spider):
    name = "qunar_area_list"
    qunar_area_sorted = 0
    allowed_domains = ["qunar.com"]
    start_urls = ["http://travel.qunar.com/p-sx1?area=1&month=0&tag=0&hot=0"]
    def start_requests(self):
        yield Request(url = self.start_urls[0], callback = self.area_list_parse)

    def area_list_parse(self, response):
        sel = Selector(response)
        url_item = UrlItem()
        url_item["source"] = "qunar"
        url_item["classes"] = "poi_list"
        name_list = sel.xpath("//div[@class='titbox']//span[@class='tit']//text()").extract()
        area_parent_list = sel.xpath("//span[@class='area']/text()").extract()
        url_list = sel.xpath("//a[@class='imglink']//@href").extract()
        url_item["url"] = url_list
        yield url_item
        picture_list = sel.xpath("//div[@class='imgbox']/a/img[@class='img']//@src").extract()
        des_list = sel.xpath("//div[@class='desbox']/text()").extract()
        for index, values in enumerate(name_list):
            item = QunarAreaListItem()
            url = url_list[index]
            self.qunar_area_sorted += 1
            item["site_sorted"] = self.qunar_area_sorted
            item["url"] = url
            item["id"] = re.findall("p-cs(\d+)-",url_list[index])[0]
            item["crawl_time"] = time.asctime(time.localtime(time.time()))
            item["name"] = name_list[index]
            item["area_parent"] = area_parent_list[index]
            item["avatar"] = picture_list[index]
            item["abstract"] = des_list[index].strip()
            item["poi_url"] = url + "-jingdian"
            item["hotel_url"] = url + "-jiudian"
            item["food_url"] = url + "-meishi"
            item["shopping_url"] = url + "-gouwu"
            item["road_url"] = url + "-xianlu"
            item["guide_url"] = url + "-zhinan"
            yield item
        next_page_url = sel.xpath("//a[@class='page next']//@href").extract()
        if next_page_url:
            yield Request(url=next_page_url[0], callback=self.area_list_parse)

class QunarPoiListSpider(scrapy.Spider):

    name = "qunar_poi_list"
    qunar_poi_sorted = {}
    allowed_domains = ["qunar.com"]
    r = Redis()
    start_urls = ["{}-jingdian".format(url) for url in r.get_set_members(name)]

    def parse(self, response):
        sel = Selector(response)
        poi_item = UrlItem()
        poi_item["source"] = "qunar"
        poi_item["classes"] = "poi_url_list"
        poi_item["url"] = parse_data_kit.xpath_parse_data(sel, "//li[@class='item']/a[@data-beacon='poi']/@href")
        yield poi_item
        area_id = parse_data_kit.re_parse_data(response.url, "p-cs(\d+)-")
        poi_des_list = sel.xpath("//ul[@class='list_item clrfix']/li[@class='item']")

        for x in poi_des_list:
            dic = QunarPoiListItem()
            dic['crawl_time'] = time.asctime(time.localtime(time.time()))
            url = parse_data_kit.xpath_parse_data(x, ".//div[@class='titbox clrfix']/a/@href")
            dic["url"] = url
            dic['area_id'] = area_id
            if area_id in self.qunar_poi_sorted:
                self.qunar_poi_sorted[area_id] += 1
            else:
                self.qunar_poi_sorted[area_id] = 1
            dic["site_sorted"] = self.qunar_poi_sorted[area_id]
            dic["id"] = parse_data_kit.re_parse_data(url, "p-oi(\d+)-")
            dic["name"] = parse_data_kit.xpath_parse_data(x, ".//div[@class='titbox clrfix']/a/span/text()")
            dic["avatar"] = parse_data_kit.xpath_parse_data(x,".//a[@data-beacon='poi']/img[@class='img']/@src")
            longitude = parse_data_kit.xpath_parse_data(x, ".//@data-lng")
            latitude = parse_data_kit.xpath_parse_data(x, ".//@data-lat")
            dic["location"] = {"lat":latitude, "lon":longitude}
            dic["en_name"] = parse_data_kit.xpath_parse_data(x, ".//span[@class='en_tit']/text()")
            dic["profile"] = parse_data_kit.xpath_parse_data(x, ".//div[@class='desbox']/text()")
            dic["rank_in_area"] = parse_data_kit.xpath_parse_data(x, ".//span[@class='ranking_sum']/span/text()")
            dic["score"] = parse_data_kit.xpath_parse_data(x, ".//span[@class='total_star']/span/@style").split(":")[1]
            dic["strategy_sum"] = parse_data_kit.xpath_parse_data(x, ".//div[@class='strategy_sum']/text()")
            dic["comment_sum"] = parse_data_kit.xpath_parse_data(x, ".//div[@class='comment_sum']/text()")
            dic["gone_rate"] = parse_data_kit.xpath_parse_data(x,".//span[@class='comment_sum']/span[@class='sum']/text()")
            yield dic

        next_page_url = parse_data_kit.xpath_parse_data(sel, "//a[@class='page next']//@href")

        if next_page_url:
            yield Request(url = next_page_url, callback = self.parse, dont_filter=False)





if __name__ == '__main__':
    pass 