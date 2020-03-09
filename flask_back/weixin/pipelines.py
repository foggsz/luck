# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.pipelines.images import   ImagesPipeline
from scrapy.exceptions  import  DropItem
from scrapy.http import Request
from weixin.tool  import img_uuid    #生成图片唯一ID
from weixin.settings  import MONGO_URL
from weixin.settings  import  MONGO_DB_NAME
# from scapy.stats import stats

class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # print(item)
        if  item.get("image_urls"):
            for image_url in item['image_urls']:
                yield Request(image_url)


    def item_completed(self, results, item, info):
        image_paths = [val['path'] for ok, val in results if ok]
        if not image_paths:
            raise DropItem("没有图片不处理")
           
        item["image_path"] = image_paths
        return item 
        

    def file_path(self, request, response=None, info=None):
        ## start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        catalog = self.crawler.stats.get_value('query') or "full"
        image_guid = img_uuid(url)
        return f'{catalog}/{image_guid}.jpg'




class WeixinPipeline(object):
    table_name = 'news'
        
    def __init__ (self, mongo_uri, mongo_db, stats):
        self.stats = stats
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = MONGO_URL,
            mongo_db = MONGO_DB_NAME,
            stats = crawler.stats
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.table_name].insert_one(dict(item))
        return item

