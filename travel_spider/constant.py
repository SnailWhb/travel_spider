#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: whb
@license: Apache Licence  
@contact: 1223934389@qq.com 
@software: PyCharm 
@file: constant.py 
@time: 18-11-19 下午6:32 
"""

import datetime

# 去哪儿
class Qunar():
    ## 输出文件的相关参数
    OUT_BASE_PATH = "/home/whb/Desktop/spider/qunar_source_data/area"
    FILE_BASE_NAME = "area"

    ##数据库相关参数
    DATABASE_NAME= "qunar"
    create_collection_date = str(datetime.datetime.now().date())
    COLLECTIONS_NAME_AREAS_LIST = "area_list_{}".format(create_collection_date)
    COLLECTIONS_NAME_POI_LIST = "poi_list_{}".format(create_collection_date)
    COLLECTIONS_NAME_POI = "poi_{}".format(create_collection_date)
    COLLECTIONS_NAME_AREAS = 'area_{}'.format(create_collection_date)
    COLLECTIONS_NAME_TRAVEL = "travel_{}".format(create_collection_date)





