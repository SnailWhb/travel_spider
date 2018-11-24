#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: whb
@license: Apache Licence  
@contact: 1223934389@qq.com 
@software: PyCharm 
@file: BaseItem.py 
@time: 18-11-21 上午10:02 
"""
from scrapy import Item, Field

class BaseItemEntity(Item):
    """
    所有Item的基类
    """
    id = Field() #唯一标识
    crawl_time = Field() #爬去的时间
    site_sorted = Field() #原始数据在网站的推荐排序
    timestamp = Field()
    image_urls = Field() #需要下载图片的url链接，可迭代对象
    image_paths = Field() #图片保存的路径






if __name__ == '__main__':
    pass 