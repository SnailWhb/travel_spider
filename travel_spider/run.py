#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: whb
@license: Apache Licence  
@contact: 1223934389@qq.com 
@software: PyCharm 
@file: run.py 
@time: 18-11-20 下午2:01 
"""
from scrapy import cmdline
spider = "qunar_poi_list"


if __name__ == '__main__':
    cmdline.execute(
        "scrapy crawl {}".format(spider).split(" ")
    )