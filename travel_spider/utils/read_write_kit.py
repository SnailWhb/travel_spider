#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: whb
@license: Apache Licence  
@contact: 1223934389@qq.com 
@software: PyCharm 
@file: file_kit.py 
@time: 18-11-19 下午6:32 
"""
from ..constant import Qunar
import os
import json

class FileWriteRead(object):

    @staticmethod
    def write_html_file(id, url, text_content):
        if not os.path.exists(Qunar.OUT_BASE_PATH):
            os.makedirs(Qunar.OUT_BASE_PATH)
        filename = Qunar.OUT_BASE_PATH + "/{}-{}.html".format(Qunar.FILE_BASE_NAME,id)
        with open(filename,"w",encoding = "utf-8") as f:
            f.write(url)
            f.write("\n")
            f.write(text_content)

    @staticmethod
    def read_json_filename(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.loads(f.read())

class MongodbWriteRead(object):

    def get_area_data(self):
          pass


class RedisWriteRead(object):
    pass



if __name__ == '__main__':
    pass 