#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: whb
@license: Apache Licence  
@contact: 1223934389@qq.com 
@software: PyCharm 
@file: parse_data_kit.py 
@time: 18-11-22 上午10:22 
"""
import re
import string

def xpath_parse_data(selector_object, xpath_expression):
    """使用xpath解析数据,并对数据进行简单的逻辑处理。如果提取的内容为,则返回为""

    :param selector_object: 需要待解析的selector_object对象，
    eg:<Selector xpath="//ul[@class='list_item clrfix']/li[@class='item']" data='<li class="item" data-lat="30.580366" da'>
    :param xpath_expression: xpath表达式
    :return:提取的内容
    """
    rlt_list = selector_object.xpath(xpath_expression).extract()
    if rlt_list == []:
        return ""
    elif len(rlt_list)==1:
        source_data = rlt_list[0].strip().strip(string.punctuation)
        return  source_data
    else:
        return [x.strip().strip(string.punctuation) for x in rlt_list]


def re_parse_data(string_object, regex_expression):
    """使用正则表达式进行提取数据

    :param string_object: 需要查询的字符串
    :param regex_expression: 正则表达
    :return:
    """
    rlt = re.findall(regex_expression, string_object)
    if rlt == []:
        return ""
    elif len(rlt) == 1:
        return rlt[0]
    else:
        return rlt




if __name__ == '__main__':
    pass 