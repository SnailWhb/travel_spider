# #!/usr/bin/env python
# # encoding: utf-8
#
# """
# @version: v1.0
# @author: whb
# @license: Apache Licence
# @contact: 1223934389@qq.com
# @software: PyCharm
# @file: mongodb.py
# @time: 18-8-23 下午1:33
# """

from travel_spider.utils.read_write_kit import FileWriteRead
from pymongo import MongoClient
from scrapy.conf import settings
from elasticsearch import Elasticsearch
import redis

class Mongodb(object):
    def __init__(self, db_name, collection_name):
        self.client = MongoClient(host=settings["MONGODB_HOST"], port=settings["MONGODB_PORT"])
        self.database = self.client.get_database(db_name)
        self.db = self.database[collection_name]


    # insert data
    def insert_data_db(self, dic):
        try:
            self.db.insert_one(dic)
        except Exception as e:
            print(str(e))

    # insert many data
    def insert_many_data(self, dic_list):
        try:
            self.db.insert_many(dic_list)
        except Exception as e:
            print(str(e))

    # update data
    def update(self, dic, new_dic, is_add=False, add_many=False):
        return self.db.update(dic, new_dic, is_add, add_many)

    # update multi-document data
    def multi_update(self, dic, new_dic):
        return self.db.update_many(dic, {"$set": new_dic})

    # delete data
    def delete(self, dic):
        return self.db.remove(dic)

    # find document by condition。
    def find_many(self,dic,field_name = ""):
        if field_name == "":
            return self.db.find(dic)
        else:
            return self.db.find(dic, field_name)

    # find one document
    def find_one(self, dic, **field_name):
        if field_name == {}:
            return self.db.find_one(dic)
        else:
            return self.db.find_one(dic, field_name)

    # find count
    def find_count_by_dict(self, dic):
        return self.db.find(dic).count()

    # save document
    def save(self, dic):
        self.db.save(dic)

    def close(self):
        self.close()


class EsClient(object):

    """
    利用在python中使用es的elasticsearch模块，根据需求重构如下功能:
    create_index: 创建索引
    delete_index: 删除索引
    delete_doc_by_id: 通过id删除文档
    delete_doc_by_query: 通过查询删除文档
    index_document： 插入文档
    bulk_index_document: 批量插入文档
    update_doc_by_id: 通过id更新文档
    update_document_by_query: 通过查询更新文档
    """

    def __init__(self, client = "localhost:9200"):
        self.es = Elasticsearch(client)

    def check(self):
        """
        输出当前系统的ES信息。

        :return:
        """
        return self.es.info()

    def exists_index(self,index_name):
       return self.es.indices.exists(index_name)

    def create_index(self, index_name):
        self.es.indices.create(index_name)

    def create_index_template(self, index_name, body_filename):
        """
        创建索引.

        :param index_name: 索引名称.
        :param body_filename: 索引的分片及字段映射设置的json文件.
        :return:
        """
        if self.es.indices.exists(index_name):
            print(index_name + " index already exists.")
        else:
            body = FileWriteRead.read_json_filename(body_filename)
            self.es.indices.create(index_name, body = body)
            print(index_name + " index create success.")

    def delete_index(self, index_name):
        """
        删除索引。

        :param index_name: 需要删除的索引
        :return:
        """
        try:
           self.es.indices.delete(index_name)
        except Exception as e:
            print(e)

    def delete_doc_by_id(self, index, type, id):
        '''
        删除指定index、type、id对应的数据
        :param index:
        :param type:
        :param id:
        :return:
        '''
        self.es.delete(index=index, doc_type=type, id=id)

    def delete_doc_by_query(self, index, type, body):
         """
         通过查询删除特定的文档数据.

         :param index:
         :param body:
         :param type:
         :return:
         """
         self.es.delete_by_query(index, doc_type=type, body=body)

    def insert_document(self, index_name, body, doc_type = "doc", id=None):
        """
        插入一条数据body到指定的index、指定的type下;可指定Id,若不指定,ES会自动生成

        :param index_name: 待插入的index(dir)
        :param index_type: 待插入的type(dir)
        :param body: 待插入的文档数据(dict)
        :param id: 文档id(若没有指定，es自动生成)
        :return:
        """
        if self.exists_index(index_name) == False:
            self.create_index(index_name)
        try:
           return self.es.index(index=index_name, doc_type=doc_type, body=body, id=id)
        except Exception as e:
            print(e)

    def bulk_index_document(self, index_name, doc_type, body_list):
        """
        批量插入数据.使用bulk函数

        :param index_name: 待插入的索引名称
        :param doc_type: 待插入的索引类型
        :param body_list: 需要插入的数据[dict, dict]
        :return:
        """
        if self.exists_index(index_name)==False:
            self.create_index(index_name)
        index_dict = [{"index":{"_index":index_name, "_type":doc_type}},]*len(body_list)
        doc_list = [dict]*(len(body_list)*2)
        doc_list[::2] = index_dict
        doc_list[1::2] = body_list
        try:
            return self.es.bulk(index=index_name, doc_type=doc_type, body=doc_list)
        except Exception as e:
            print(e)

    def update_doc_by_id(self, index, id, type= "doc", body=None):
        """
        更新指定index，type，id所对应的数据.

        :param index:
        :param type:
        :param id:
        :param body: 待更新的值.eg:{"doc":dict}
        :return:
        """
        try:
           return self.es.update(index=index, doc_type=type, id=id, body=body)
        except Exception as e:
            print(e)

    def update_document_by_query(self, index, doc_type, body=None):
        """
        通过查询更新文档.

        :param index: 待更新文档的索引.
        :param doc_type: 索引类型
        :param body: 查询体及更新体
         eg:updateBody = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"_id": "11"}}
                    ],
                }
            },
            "script": {
                "inline": "ctx._source.tags = params.tags",
                "params": {
                    "tags": tags
                },
                "lang":"painless"
            }
         }
        :return:
        """
        try:
            self.es.update_by_query(index, doc_type=doc_type, body=body)
        except Exception as e:
            print(e)

    def close(self):
        if self.es is not None:
            try:
                self.es.close()
            except Exception as e:
                print(e)
            finally:
                self.es = None


class Redis(object):
    def __init__(self, host="localhost", port=6379, db = 0 ):
        self.pool = redis.ConnectionPool(host = host, port = port, db = db, decode_responses = True)
        self.db = redis.Redis(connection_pool = self.pool)

    def exists_key(self, key):
        return self.db.exists(key)
    ##String操作
    def set_mstring(self, dict_kv):
        self.db.mset(dict_kv)
    def get_mstring(self,key_list):
        return  self.db.mget(key_list)
    def set_string(self,k,v):
        self.db.set(k,v)
    def get_string(self,k):
        return self.db.get(k)
    #Set操作
    def set_set_list(self,name,values_list):
        for value in values_list:
            self.db.sadd(name, value)

    def set_set_value(self,name,value):
        self.db.sadd(name,value)

    def get_set_length(self,set_name):
        return self.db.scard(set_name)

    def get_set_members(self, name):
        return self.db.sscan_iter(name)






if __name__ == '__main__':
    # # es = EsClient(client)
    # local = "localhost:9200"
    # es = EsClient(local)
    # es.create_index("test")
    # print(es.exists_index("poi_dd"))

    # 创建创建索引
    # poi_body_filename = "/home/whb/Desktop/kmind/Data_Pre/InputData/EsMapping/poiMappingTemplate.json"
    # area_body_filename = "/home/whb/Desktop/kmind/Data_Pre/InputData/EsMapping/areaMapping.json"
    # user_body_filename = "/home/whb/Desktop/kmind/Data_Pre/InputData/EsMapping/user_mapping.json"
    # travel_body_filename = "/home/whb/Desktop/kmind/Data_Pre/InputData/EsMapping/roadline.json"
    # es.create_index("poi", poi_body_filename)
    # es.create_index("area", area_body_filename)
    # es.create_index("user_index_v2", user_body_filename)
    # es.create_index("travel", travel_body_filename)
    # client = "39.105.130.14:9222"
    # map_type = "map_v1"  # map_v1, map_v2
    # index_version = "v1"
    # index_list = ["travel","user","area","poi"]
    # self_create_index(map_type, index_list, index_version, client)

    r = Redis()

    for x in r.get_set_members("qunar_poi_list"):
        print(x)
    # r.set_string({"d":1,"d1":2})
    # print(r.get_string(["d","d1"]))





