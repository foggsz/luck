# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode, parse_qsl, quote, unquote
from scrapy  import  FormRequest
from weixin.tool import USER_AGENT
import time
import pymongo
from weixin.settings  import  MONGO_URL
from weixin.settings  import  MONGO_DB_NAME
from weixin.loader  import wxLoader, wxDetailLoader
from weixin.items   import wxItems, wxDetailItems
import re
import json
import logging
from scrapy import signals
from scrapy.utils.log import configure_logging
from scrapy.exceptions  import CloseSpider
from twisted.internet import reactor
from scrapy.signalmanager import SignalManager

mysignal = SignalManager()
my_signals = {
    'error': object(),
    "isLoadImage": object(),
    "finished": object(),
    "record": object(),  #记录失败
    "record_success": object()       #成功时抹去失败
}


class WxSpider(scrapy.Spider):
    name = 'wx'
    allowed_domains = ['weixin.qq.com', "baidu.com"]
    query_params = {}
    custom_settings = {
        # 'LOG_FILE': '../wx.log',
        # 'LOG_LEVEL': 'DEBUG',
        # 'LOG_STDOUT': False,
        "ITEM_PIPELINES":{
            "weixin.libs.mongopipe.mediaPipeline":299,   
            "weixin.libs.mongopipe.MongoPipeline":300,
        },
        "DOWNLOAD_DELAY": 2,
        # "EXTENSIONS":{
        #     "weixin.libs.extension.SpiderOpenCloseLogging":600,
        # }
        # "IMAGES_STORE": "../images"
    }

    logFormatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()     
    handlerInfo  = logging.handlers.RotatingFileHandler('../wx.log', maxBytes=1000000000,  backupCount=100, encoding="utf-8")
    handlerInfo.setLevel(logging.DEBUG)
    handlerInfo.setFormatter(logFormatter)
    handlerError = logging.handlers.RotatingFileHandler('../wx_error.log', maxBytes=1000000000,  backupCount=100, encoding="utf-8")
    handlerError.setLevel(logging.WARNING)
    handlerError.setFormatter(logFormatter)
    logger.addHandler(handler)
    logger.addHandler(handlerInfo)
    logger.addHandler(handlerError)
    start_urls = ["https://mp.weixin.qq.com/mp/profile_ext?"]
    def __init__(self,*args, **kw): 
        self.kw = kw      #抓取条件
        #extra =  ["allLoad"] 爬虫其他条件   allLoad全部重新下载
        extra = self.kw.get("extra") or [] #其他条件
        self.allLoad = True if "allLoad" in extra else False
        self.client = pymongo.MongoClient(MONGO_URL)
        self.db  = self.client[MONGO_DB_NAME]
        self.source = self.db["source"]
        self.__biz  = None      #组织Id
        self.lastest_one = None   #上次抓取最后一条文档
        self.query_url = None   #查询地址
        self.cookies  = None
        self.count = 10
        self.offset = 0
        self.org_name =  0
        self.switch_dicts = {
            "list": self.list_requests(),
            "detail": self.detail_requests()
        }

        
    def start_requests(self, ):  
        condition = self.kw.get("condition") 
        if condition in self.switch_dicts:
            mysignal.send_catch_log(signal= my_signals.get("isLoadImage"), spider=self, isLoadImageBool=self.kw.get("isLoadImage"))
            return self.switch_dicts[condition]
        else:
            return mysignal.send_catch_log(signal= my_signals.get("error"), spider=self, reason=self.kw.get("keyword")+'，'+"没有对应的条件")
            return scrapy.Request("https://www.baidu.com", callback=self.close_spider, errback=self.close_spider)

    def close_spider(self, response):
        print(response)

    def detail_requests(self, ):
        self.crawler.stats.set_value('collection_name', "article.detail")   #设置插入的表名
        self.where  = {
            "NickName":self.kw["keyword"]
        }
        try:
            article_urls =  self.detail_list()
        except ValueError as e:
            self.logger.error(str(e))
            mysignal.send_catch_log(signal= my_signals.get("error"), spider=self, reason=self.kw.get("keyword")+'，'+str(e) )
            mysignal.send_catch_log(signal= my_signals.get("record"), spider=self, **{'biz_id': self.__biz, 'status':'fail'} )
            time.sleep(0.8)
            return 
        collection_name = self.crawler.stats.get_value("collection_name")
        self.lastest_one =  self.get_lastone(self.db[collection_name], self.__biz)
        for item in article_urls:
            content_url = item.get("content_url")
            yield scrapy.Request(content_url, meta={
                    "biz_id": item.get("biz_id"),
                    "list_id": item.get("_id"),
                    "pub_time": item.get("pub_time"),
                    "content_url": content_url
                }, callback=self.parse_detail
            )

        self.logger.info(self.kw.get("keyword")+"详情页文章已经抓取完毕")
        mysignal.send_catch_log( signal= my_signals.get("finished"), spider=self, reason="{0}:详情页文章已经抓取完毕:finished".format(self.kw.get("keyword")) )
        return 

    def list_requests(self, ):
        self.crawler.stats.set_value('collection_name', "article.list")   #设置插入的表名
        self.where = {
            "$or":[
                { "__biz":{"$regex": self.kw["keyword"] , "$options": "i" } },
                { "NickName":self.kw.get("keyword") }
            ]
        }
        try:
            appmsg_token = self.get_source(self.where)
        except ValueError as e:
            self.logger.error(str(e))
            mysignal.send_catch_log(signal= my_signals.get("error"), spider=self, reason=self.kw.get("keyword")+'，'+str(e))
            mysignal.send_catch_log(signal= my_signals.get("record"), spider=self,**{'biz_id':self.__biz, 'status':'fail'})
            time.sleep(0.8)
            
            return
        
        collection_name = self.crawler.stats.get_value('collection_name')
        self.lastest_one = self.get_lastone(self.db[collection_name], self.__biz) #上次抓取最后一个文档

        for url in self.start_urls:    

            self.query_url  =  f"action=getmsg&__biz={self.__biz}&f=json&offset={self.offset}&count={self.count}&appmsg_token={appmsg_token}" 
            url  =  url + self.query_url
            yield scrapy.Request(url,
                headers={
                "Referer": f"https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={self.__biz}"
                },
                cookies = self.cookies,
                callback= self.parse
            )

    def get_lastone(self,collection,  biz_id):
        lastest_one = collection.find({'biz_id':biz_id},{"fileid":1, "list_id":1, "pub_time":1 }).sort("pub_time", -1).limit(1)
        lastest_one = list(lastest_one)
        if  len(lastest_one) ==0:
            lastest_one = {}
        else:
            lastest_one = lastest_one[0]
        return lastest_one

    def get_source(self, where):
        source_data = self.source.find_one(where, {"Host":1, "Connection":1, "Content-Length":1, "Origin":1, "X-Requested-With":1, "User-Agent":1, "wap_sid2":1,
                "Content-Type":1, "Accept":1, "Referer":1, "Accept-Encoding":1, "Accept-Language":1, "Cookie":1, "Q-UA2":1, "Q-GUID":1, "Q-Auth":1, "_id":0,"__biz":1,
                "appmsg_token":1, "NickName": 1,
                 "_id":0

            })
        if  source_data is None:
            raise ValueError("没有找到对应的公众号")

        appmsg_token = source_data["appmsg_token"]
        self.__biz  = source_data["__biz"]
        self.org_name = source_data["NickName"]
        cookies  = source_data["Cookie"]
        cookies  =  cookies.replace(";","&")
        self.cookies = dict( parse_qsl(cookies) )
        self.cookies["wap_sid2"] = source_data.get("wap_sid2") 
        return  appmsg_token


    def refresh_appmsg_token(self, ):
        token =  self.source.find_one(self.where, {
            "appmsg_token":1
        })
        return token["appmsg_token"]
        
    def parse(self, response):
        res = response.body_as_unicode()
        need_verify =  re.search("\<title\>验证\<\/title\>", res)
        if need_verify  is None:
            res =  res.replace('"{',"{")
            res =  res.replace('}"',"}")
            res =  res.replace("\\","")
            res  = json.loads(res) or {}
            # base_resp = res.get("base_resp")   #通用回复
            errmsg = res.get("errmsg") 

        resTry = False    #重新抓取条件
        if  need_verify is not None   or  res is None or errmsg != "ok" or errmsg is None :
            resTry  = True
        if  resTry:
            self.crawler.stats.inc_value('retry_count')
            if self.crawler.stats.get_value("retry_count") > 1:
                error_info = "{0}:凭证失效,请重新获取凭证".format(self.kw.get("keyword")) 
                if type(res)  == dict:   #未知错误  操作频繁限制
                    if res.get("ret")  == -6:
                        error_info = "{0}:微信帐号操作被限制，请换号重试".format(self.kw.get("keyword")) 

                self.logger.info(error_info)
                mysignal.send_catch_log(signal= my_signals.get("record"), spider=self, **{"biz_id": self.__biz, 'status':'fail'})
                raise CloseSpider(reason=error_info)

            self.logger.info("两秒后重新爬取")
            time.sleep(2)
            appmsg_token = self.refresh_appmsg_token()
            retry_url = response.url
            retry_url =  re.sub("appmsg_token=(.*)", f"appmsg_token={appmsg_token}", retry_url)
            yield scrapy.Request(retry_url,
                    headers = {
                        "User-Agent": USER_AGENT
                    },
                    cookies = self.cookies,
                    callback=self.parse,
                    dont_filter=True
            )     
            return  

        if res.get("general_msg_list"): 
            if res.get("general_msg_list").get("list"):
                for item in res["general_msg_list"]["list"]:
                    l = wxLoader(item=wxItems())
                    pub_time  =  None
                    article_type  = None
                    if  item.get("comm_msg_info"):    # comm_msg_info  公众号文章通用消息   type 1 49
                        pub_time  = item["comm_msg_info"].get("datetime") 
                        article_type  =  item["comm_msg_info"].get("type")
                        if  article_type == 1 and item["comm_msg_info"].get("content").strip()!="":
                            fakeid  =  item["comm_msg_info"].get("fakeid")
                            fakeid  = int(fakeid)  if fakeid is not None else None

                            if not self.allLoad: #不需要全部下载才进行最新日期抓取，针对更新，针对重新采集
                                if self.lastest_one.get("fakeid") and self.lastest_one.get("fakeid") == fakeid:
                                    raise CloseSpider(reason="{0}:列表页更新完成:finished".format(self.kw.get("keyword")))

                            l.add_value("fileid", fakeid)    #把有内容的通用消息 转化为单个文章，fakeid为文章ID 
                            l.add_value("comm_msg_info", item.get("comm_msg_info"))
                            l.add_value("article_type", article_type)
                            l.add_value("biz_id", self.__biz)
                            yield l.load_item() 

                    if item.get("app_msg_ext_info"):
                        l.add_value("title", item["app_msg_ext_info"].get("title"))
                        l.add_value("author", item["app_msg_ext_info"].get("author"))
                        l.add_value("content_url", item["app_msg_ext_info"].get("content_url"))
                        l.add_value("source_url", item["app_msg_ext_info"].get("source_url") )
                        l.add_value("cover", item["app_msg_ext_info"].get("cover") )
                        l.add_value("image_urls", item["app_msg_ext_info"].get("cover") )
                        l.add_value("fileid", item["app_msg_ext_info"].get("fileid")) 
                        l.add_value("comm_msg_info", item.get("comm_msg_info"))                        
                        l.add_value("pub_time", pub_time)
                        l.add_value("biz_id",  self.__biz)
                        l.add_value("article_type", article_type) 
                        l.add_value("org_name", self.org_name)
                        result =  l.load_item()

                        if not self.allLoad: #不需要全部下载才进行最新日期抓取，针对更新，针对重新采集
                            if self.lastest_one.get("fileid") and self.lastest_one.get("fileid") == result.get("fileid"):   
                                mysignal.send_catch_log( signal= my_signals.get("record_success"), spider=self, **{"biz_id": self.__biz} ) 
                                raise CloseSpider(reason="{0}:列表页更新完成:finished".format(self.kw.get("keyword")))

                        yield result
                        if item["app_msg_ext_info"].get("multi_app_msg_item_list"):
                            for  val in item["app_msg_ext_info"]["multi_app_msg_item_list"]:
                                l = wxLoader(item=wxItems())
                                l.add_value("title", val.get("title"))
                                l.add_value("author", val.get("author")) 
                                l.add_value("fileid", val.get("fileid")) 
                                l.add_value("content_url", val.get("content_url"))
                                l.add_value("source_url", val.get("source_url"))
                                l.add_value("cover", val.get("cover"))
                                l.add_value("image_urls", val.get("cover") )
                                l.add_value("org_name", self.org_name)
                                # if val.get("cover"):
                                #     l.add_value("image_urls", val.get("cover") )
                                l.add_value("comm_msg_info", item.get("comm_msg_info"))
                                l.add_value("pub_time", pub_time)
                                l.add_value("biz_id",  self.__biz)
                                l.add_value("article_type", article_type) 
                                result = l.load_item()
                                yield result
            

            next_offset  = res.get("next_offset")
            is_more = int(self.count) + int(self.offset)   #文章最大数量
            if  next_offset is None  or next_offset < is_more:
                self.logger.info(self.kw.get("keyword")+"列表页文章已经抓取完毕")
                mysignal.send_catch_log( signal= my_signals.get("record_success"), spider=self, **{"biz_id": self.__biz} ) 
                raise CloseSpider(reason="{0}:列表页文章已经抓取完毕:finished".format(self.kw.get("keyword")))
                return 
            else:
                self.offset = next_offset
                next_url =  response.url
                next_url = re.sub("offset=(.*)&", f"offset={self.offset}&", next_url)
                yield response.follow(next_url, callback= self.parse)


    def detail_list(self, ):  #文章源
        bizData = self.source.find_one(self.where, {
            "__biz":1
        })
        if bizData is None or bizData.get("__biz") is None:
            raise ValueError("没有对应的公众号")

        self.__biz = bizData.get("__biz")
        article_urls = self.db["article.list"].find({"biz_id" : self.__biz, "content_url": {"$exists":True } },{
            "content_url": 1,
            "biz_id": 1,
            "_id" :1,
            "pub_time":1
        })
        article_urls = list(article_urls)
        if article_urls is None or  len(article_urls) ==0:
            raise ValueError("没有对应的公众号")

        return article_urls



    def parse_detail(self, response):  #抓取文章详情页
        # raise CloseSpider('today scrapy end')
        body = response.body_as_unicode()
        meta = response.meta
        l = wxDetailLoader(item=wxDetailItems(), response=response)
        pub_time = meta.get("pub_time")
        list_id = meta.get("list_id")
        if not self.allLoad: #不需要全部下载才进行最新日期抓取，针对更新，针对重新采集
            if self.lastest_one.get("list_id") and self.lastest_one.get("list_id") == list_id: 
                raise CloseSpider(reason="{0}:详情页更新完成:finished".format(self.kw.get("keyword")))

        biz_id = meta.get("biz_id")
        content_url = meta.get("content_url") 
        l.add_css("title", "h2#activity-name")
        l.add_css("author", "a#js_name")
        l.add_css("content", "div#js_content")
        l.add_value("pub_time",  f"{pub_time}")
        l.add_value("list_id",  f"{list_id}")
        l.add_value("biz_id",  f"{biz_id}")
        l.add_value("content_url", f"{content_url}")
        l.add_css("image_urls", "img::attr(data-src)")
        l.add_css("image_urls", "img::attr(src)")
        res = l.load_item()       
        yield res






