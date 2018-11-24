# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from travel_spider.utils.base_item import BaseItemEntity,Field
from scrapy import Item

class UrlItem(Item):
    """将待爬去的url队列存储到redis"""
    id = Field() #url的唯一标识
    url = Field() #待爬去的url
    source = Field() #url的来源:qunar,xiecheng,baidu,tuniu,...
    classes = Field() # poi, area, route, poi_list, area_list,...


class QunarAreaListItem(BaseItemEntity):
    """去哪儿网上的区域列表数据模型"""

    name = Field() #区域名称
    url = Field()  # 原始数据的url链接
    area_parent = Field() #上一级区域名称
    avatar = Field()  # 头图
    abstract = Field() #区域简介
    poi_url = Field() #区域景点url
    food_url = Field() #美食
    shopping_url = Field() #购物
    road_url = Field() #路线
    hotel_url = Field() #酒店
    guide_url = Field() #指南


class QunarPoiListItem(BaseItemEntity):
    """去哪儿上的景点列表的数据模型"""
    url = Field()  #景点url
    name = Field() #景点名称
    area_id = Field() #所属区域id
    en_name = Field() #英文名称
    longitude = Field() #经度
    latitude = Field() #纬度
    comment_sum = Field() #评论总数
    strategy_sum = Field() #攻略数
    rank_in_area = Field() #在区域中的排序
    score = Field() #评分
    avatar = Field()  #头图
    gone_rate = Field() #去过该区域的人，有多少比例人去过该景点
    profile = Field() #一句话简介
    location = Field()


class QunarPoiItem(BaseItemEntity):
    """去哪儿网上，景点详情"""
    pass













if __name__ == '__main__':
    area = QunarAreaListItem()
    area["_id"] = "1"
    print(area["_id"])
    poi_list = QunarPoiListItem()
    poi_list["name"] = 355
    print(type(poi_list['name']))


