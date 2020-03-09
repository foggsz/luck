# # -*- coding: utf-8 -*-
# import scrapy
# from urllib.parse import urlencode, parse_qsl
# import chardet
# from scrapy  import  FormRequest
# from weixin.lib import USER_AGENT
# import time
# import pymongo
# from weixin.settings  import  MONGO_URL
# from weixin.settings  import  MONGO_DB_NAME
# from weixin.loader  import wxLoader
# from weixin.items   import wxItems
# import re
# import json
# class WxSpider(scrapy.Spider):
#     name = 'wx2'
#     allowed_domains = ['weixin.qq.com']
    
#     query_params = {
#         "action": "home"     #必传


#     }
    
#     custom_settings = {
#         "ITEM_PIPELINES":{
#             "weixin.myMiddlewares.mongopipe.MongoPipeline":300
#         }
#     }

#     start_urls = ["https://mp.weixin.qq.com/mp/profile_ext?"]



#     def __init__(self):
#         self.client = pymongo.MongoClient(MONGO_URL)
#         self.db  = self.client[MONGO_DB_NAME]
#         self.collction = self.db["source"] 
#         self.logger.setLevel("INFO")


#     # #重写
#     # def start_requests(self):
#     #     params = ""
#     #     for url in self.start_urls:
#     #         source_data = self.collction.find_one({}, {"Host":1, "Connection":1, "Content-Length":1, "Origin":1, "X-Requested-With":1, "User-Agent":1, 
#     #             "Content-Type":1, "Accept":1, "Referer":1, "Accept-Encoding":1, "Accept-Language":1, "Cookie":1, "Q-UA2":1, "Q-GUID":1, "Q-Auth":1, "_id":0,"__biz":1
#     #         })

#     def start_requests(self):
#         params = ""
#         for url in self.start_urls:
#             source_data = self.collction.find_one({}, {"Host":1, "Connection":1, "Content-Length":1, "Origin":1, "X-Requested-With":1, "User-Agent":1, 
#                 "Content-Type":1, "Accept":1, "Referer":1, "Accept-Encoding":1, "Accept-Language":1, "Cookie":1, "Q-UA2":1, "Q-GUID":1, "Q-Auth":1, "_id":0,"__biz":1
#             })
#             cookies  = source_data["Cookie"]
#             cookies  =  cookies.replace(";","&")
#             self.cookies = dict( parse_qsl(cookies) )
#             self.query_params["__biz"] = source_data["__biz"]
#             url = url + urlencode(self.query_params)
#             print(url)
#             yield scrapy.Request(url ,
#                 cookies = self.cookies, meta={
#                 "__biz": self.query_params["__biz"]
#             })
        
#     def parse(self, response):
#         print("7878787878787878787878877878787878788787211212123")
#         print(response.status)
#         body = response.body_as_unicode()
#         msgList = re.search("var+\s*msgList+\s*\=+(.*[&quto]*);",body)
#         print("bodudududududu")
#         print(response.request.headers)
#         try:
#             res = re.search("页面无法打开", body)
#             if res is None:
#                 msgList = msgList.group(1)
#                 msgList = re.sub("(&quot;|quot)*(&amp|amp|;)*\s*","",msgList)
#                 msgList = msgList.replace("{", '{"')
#                 msgList = msgList.replace(",", ',"')
#                 msgList = msgList.replace(",", '",')
#                 msgList = msgList.replace(":", '":')
#                 msgList = msgList.replace(":", ':"')
#                 msgList = msgList.replace("}", '"}')
#                 msgList = msgList.replace('http":"', 'http:')
#                 msgList = msgList.replace('https":"', 'https:')
#                 msgList = msgList.replace('https":"', 'https:')
#                 msgList = msgList.replace('"[', '[')
#                 msgList = msgList.replace(']"', ']')
#                 msgList = msgList.replace('"{', '{')
#                 msgList = msgList.replace('}"', '}')
#             else:
#                 self.logger.error("爬取失败，两秒后重试")
#                 raise AttributeError("爬取失败")

#         except AttributeError as e:
#             time.sleep(2)
#             print(self.cookies)
#             yield scrapy.Request(response.url,
#                     headers = {
#                         "User-Agent": USER_AGENT
#                     },
#                     cookies = self.cookies,meta={
#                     "__biz": self.query_params["__biz"]
#                     },callback=self.parse,dont_filter=True
#                 )
#         except  Exception as e:
#             self.logger.error("内容不对，转义错误") 

#         if msgList is None:          
#             return 

#         msgList =  msgList.replace("'","")
#         msgList =  json.loads(msgList) 
#         print("lelellennnn")
#         print(len(msgList["list"]))
#         try:
#             for item in msgList["list"]:
#                 __biz = response.meta["__biz"]
#                 l = wxLoader(item=wxItems()) 
#                 l.add_value("title", item["app_msg_ext_info"].get("title"))
#                 l.add_value("author", item["app_msg_ext_info"].get("author"))
#                 l.add_value("content_url", item["app_msg_ext_info"].get("content_url"))
#                 l.add_value("source_url", item["app_msg_ext_info"].get("source_url") )
#                 l.add_value("cover", item["app_msg_ext_info"].get("cover") )
#                 l.add_value("fileid", item["app_msg_ext_info"].get("fileid")) 
#                 l.add_value("comm_msg_info", item.get("comm_msg_info"))
#                 l.add_value("pup_time", item["comm_msg_info"].get("datetime"))
#                 l.add_value("bizId",  __biz)
#                 res = l.load_item()
#                 self.crawler.stats.inc_value('a')
#                 yield res

#                 if item["app_msg_ext_info"].get("multi_app_msg_item_list"):
#                     for  val in item["app_msg_ext_info"]["multi_app_msg_item_list"]:
#                         self.crawler.stats.inc_value('b')
#                         l = wxLoader(item=wxItems())
#                         l.add_value("title", val.get("title"))
#                         l.add_value("author", val.get("author")) 
#                         l.add_value("fileid", val.get("fileid")) 
#                         l.add_value("content_url", val.get("content_url"))
#                         l.add_value("source_url", val.get("source_url"))
#                         l.add_value("cover", val.get("cover"))
#                         l.add_value("comm_msg_info", item.get("comm_msg_info"))
#                         l.add_value("pup_time", item["comm_msg_info"].get("datetime"))
#                         l.add_value("bizId",  __biz)
#                         res = l.load_item()
#                         yield res

#         except Exception as e:
#             self.logger.error("发生未知错误,请检查日志")
#             raise
#         url = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzIzNTIzMTYzOQ==&f=json&offset=46&count=10&appmsg_token=978_fsuZQlLeHSfDm5XJbjxuGTZ8qGr259u4nr6YHQ~~&x5=1&f=json"
#         yield response.follow(url,callback=self.parse_list)


    
#     def  parse_list(self, response):
#         print("headersssssssffdsfd")
#         print(response.request.headers)
#         body = response.body_as_unicode()
#         print(body)
