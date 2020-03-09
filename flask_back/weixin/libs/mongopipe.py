import pymongo
from datetime import datetime
from bson import  ObjectId
import logging
from  scrapy.exceptions  import  DropItem
from  scrapy import Request
from weixin.tool  import img_uuid    #生成图片唯一ID
from scrapy.pipelines.images import   ImagesPipeline
from scrapy  import Selector
from  weixin.loader import handle_img_urls
from weixin.spiders.wx import mysignal, my_signals
import re
from config import BASE_URL
from app.utils import search_city
logger = logging.getLogger(__name__)
isLoadImage  = False
def  isLoadImageSingal(spider, isLoadImageBool):
    global  isLoadImage
    if isLoadImageBool:
        isLoadImage = isLoadImageBool

mysignal.connect(isLoadImageSingal, signal=my_signals.get("isLoadImage"))
#处理图片
class mediaPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        self.catalog =  item.get("biz_id")
        if isLoadImage:
            if item.get("image_urls"):
                for image_url in item['image_urls']:
                    yield Request(image_url)
        
    def item_completed(self, results, item, info):        
        image_paths = [val['path'] for ok, val in results if ok]
        if not image_paths and isLoadImage and len(image_paths)!=0:
            raise DropItem("没有图片不处理")

        item["image_paths"] = image_paths    
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

        catalog = self.catalog  if self.catalog else "full"
        image_guid = img_uuid(url)
        return f'{catalog}/{image_guid}.jpg'




#数据表名字
collections = ["article.list",  "article.detail"]
class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db, stats):
        self.stats = stats
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URL'),
            mongo_db = crawler.settings.get('MONGO_DB_NAME', 'items'),
            stats = crawler.stats,
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = self.stats.get_value("collection_name")
        where = {}
        if item.get("list_id"):
            item["list_id"]  =  ObjectId(item["list_id"])
        fileid  = item.get("fileid")
        biz_id  = item.get("biz_id")
        content_url = item.get("content_url")
        item = dict(item)
        item.update({
            "updateAt": datetime.utcnow()
        })
        '''
        对文章列表和文章详情表进行处理
        '''

        if collection_name   in collections:
            if collection_name == "article.detail":
                where = {
                    "$or":[
                        {
                            "content_url":content_url
                        },
                    ]
                }
                if item.get("content"):
                    content = item.get("content")
                    item["content"] = content.replace("data-src", "src")
                img_paths = item.get("image_paths")  #修改内容图片地址为下载好的地址
                if img_paths is not None  and item.get("biz_id") is not None:
                    try:                       
                        img_replace_urls = Selector(text = item.get("content")).css("img::attr(src)").extract()
                    except Exception as e:
                        logger.error("没有找到图片")
                    else:   
                        for url in img_replace_urls:
                            temp_url = handle_img_urls(url)
                            sha1_url = img_uuid(temp_url)
                            path_url  =  item.get("biz_id")+"/"+sha1_url+".jpg"
                            if path_url in img_paths:
                                path_url =  BASE_URL + "upload/" + path_url
                                item["content"]  = item["content"] .replace(url, path_url)

                
                
            elif collection_name == "article.list":
                where = {
                    "$and":[
                        {
                            "fileid": fileid,         
                        },
                        {
                            "biz_id": biz_id
                        }
                    ]
                }
                if item.get("image_paths") and item.get("cover") and len(item.get("image_paths")) > 0:
                    item["cover"] =  BASE_URL + "upload/" + item.get("image_paths")[0]
                    
        else:
            raise DropItem("不存在的表")                    #不会进行处理
        
        self.db[collection_name].update_one(where, {"$set":item}, upsert=True)
        # old_data = self.db[collection_name].find_one(where, {"_id":1})
        # if not old_data:
        #     # self.db[collection_name].update_one(where, {"$set":item}, upsert=True)
        #     self.db[collection_name].insert(item)
        # else:
        #     if item.get("image_paths"):
        #         self.db.update_one(where, {"$set":item} )
        return item


class SocietyMongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db, stats):
        self.stats = stats
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
   
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URL'),
            mongo_db = crawler.settings.get('MONGO_DB_NAME', 'items'),
            stats = crawler.stats,
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db["society"]

    def close_spider(self, spider):
        self.client.close()
    
    def process_item(self, item, spider):
        item.setdefault('updateAt', datetime.utcnow())
        org_id = item.get("org_id")
        if org_id:
            where = { "org_id": org_id}
        else:
            where =  {
                    "i": item.get("i"),
                    "u": item.get("u")
                }

        temp_org_tag = item.get("org_tag")  #针对数组
        if temp_org_tag:
            item.pop("org_tag", None)
            setItems = {
                "$set":item,
                "$addToSet":{ "org_tag": {"$each": temp_org_tag } }
            }
        else:
            setItems = {"$set": item}
        
        self.collection.update_one(where, setItems, upsert=True)
        return item


class GSLMongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db, stats):
        self.stats = stats
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
   
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URL'),
            mongo_db = crawler.settings.get('MONGO_DB_NAME', 'items'),
            stats = crawler.stats,
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db["gsl"]

    def close_spider(self, spider):
        self.client.close()
    
    def process_item(self, item, spider):
        item.setdefault('updateAt', datetime.utcnow())
        detail_url = item.get("detail_url")
        if detail_url:
            where = { "detail_url": detail_url}
            setTtem = {
                "$set": item
            }
            self.collection.update_one(where, setTtem, upsert=True)
        # else:
        #     self.collection.insert_one(item)

        return item