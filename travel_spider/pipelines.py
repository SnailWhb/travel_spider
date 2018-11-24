# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .utils.database_kit import Mongodb,EsClient,Redis
from .constant import Qunar
from scrapy.conf import settings
from .items import QunarAreaListItem,QunarPoiListItem,UrlItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem

class HtmlWriterPipeline(object):
    def open_spider(self):
        self.f = open("qunar_area.html","w", encoding="utf-8")

    def close_spider(self):
        self.f.close()

    def process_item(self, item, spider):
        return item

class MongodbPipeline(object):
    area_list_set = set()
    poi_list_set = set()

    def __init__(self):
        self.area_list = Mongodb(Qunar.DATABASE_NAME, Qunar.COLLECTIONS_NAME_AREAS)
        self.poi_list = Mongodb(Qunar.DATABASE_NAME, Qunar.COLLECTIONS_NAME_POI)

    def close_spider(self, spider):
        self.area_list.close()
        self.poi_list.close()


    def process_item(self, item, spider):
        if isinstance(item, QunarAreaListItem):
            id = item["id"]
            if id not in self.area_list_set:
              self.area_list.insert_data_db(dict(item))
              self.area_list_set.add(id)
            else:
                raise DropItem("Duplicate id found: %s" % item["id"])
        elif isinstance(item,QunarPoiListItem):
            id = item["id"]
            if id not in self.poi_list_set:
                self.poi_list.insert_data_db(dict(item))
                self.poi_list_set.add(id)
            else:
                raise DropItem("Duplicate id found: %s" % item["id"])

class ElasticsearchPipeline(object):
    """将爬去的数据存储到"""

    def __init__(self):
        self.es = EsClient()
    def process_item(self, item, spider):
        if isinstance(item, QunarAreaListItem):
            id = item["id"]
            self.es.insert_document(Qunar.COLLECTIONS_NAME_AREAS_LIST, dict(item), id=id)
        elif isinstance(item, QunarPoiListItem):
            id = item["id"]
            self.es.insert_document(Qunar.COLLECTIONS_NAME_POI_LIST, dict(item), id=id)
        return item

class RedisPipeline(object):
    """将url保存到redis"""
    def __init__(self):
        self.db = Redis()
    def process_item(self, item, spider):
        if isinstance(item, UrlItem):
            name = "{}_{}".format(item["source"],item["classes"])
            self.db.set_set_list(name, item["url"])
        return item

class ImagesDownloadPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(url = image_url)


    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item



class DuplicatesPipeline(object):
    """Item去重复"""

    def __init__(self):
        self.r = Redis()

    def process_item(self, item, spider):
        if not isinstance(item, UrlItem):
            if self.r.exists_key('url:%s' % item['url']):
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.r.set_string('url:%s' % item['url'], 1)
        return item


