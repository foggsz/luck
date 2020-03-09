# -*- coding: utf-8 -*- 
import re
# import certifi
# import urllib3
# from mitmproxy import proxy, options
# from mitmproxy.tools.dump import DumpMaster
from  mitmproxy  import flowfilter, http, proxy, options
from sshtunnel import SSHTunnelForwarder
from pymongo import MongoClient
from urllib.parse import  parse_qsl, parse_qs
from bs4 import BeautifulSoup
from datetime  import datetime
import urllib.parse
import json
import chardet
import sys
import requests
from threading import Timer, Lock
import os
import time
# http = urllib3.PoolManager(
#     cert_reqs='CERT_REQUIRED',
#     ca_certs=certifi.where())
# try:
#     r = requests.get("http://www.baidu.com/")

# except Exception as e:
#     print(e)

def my_parse_qsl(params):
    array = params.split("&")
    res = { item[0]:item[1] for item in [ i.split("=")  for i in array ] }
    return res


to_update_list = False
# REMOTE_SERVER_IP = "47.104.150.23"

# print(server.local_bind_port)
loginData = {
    "username": "spider_admin",
    "password":  123456
}
Base_url = "https://wx.hnzhixi.com/"
# Base_url = "http://127.0.0.1:8000/"
token = None

def update_login_func():
    global token
    global to_update_list
    to_update_list = True
    r = requests.post(Base_url+"/api/user/login", data = loginData, verify=False)
    res = r.json()
    token  = res.get("token")
    print(token)

def update_list_func(keyword):
    global token
    headers = {'Authorization': token}
    post_params = {
        "keyword": keyword,
        "condition": 'list',
        "isLoadImage": 'false'
    }
    r = requests.post(Base_url+"/api/wx/spider", data = post_params, headers=headers, verify=False)
    json_r = r.json()
    if json_r.get("returnToken"):
        token = json_r.get("returnToken")
    if json_r.get("coode"):
        if json_r.get("coode") == 5001 or json_r.get("coode") == 5002 or json_r.get("coode") == 5003:
            update_login_func()
            time.sleep(4)

if "g" in sys.argv:
    global Timer
    Timer(5, update_login_func).start()

class FetchSourceParam(object):
    def __init__(self):
        self.nickName = None
        self.__biz  = None
        self.appmsg_token  = None
        self.cookie = None
        self.new_headers= dict()
        self.wap_sid2 = None
        self.count =  0
        # server = SSHTunnelForwarder(
        #     ("47.104.150.23", 22),  
        #     ssh_username="root",
        #     ssh_pkey="/Users/pingguo1zhixi/.ssh/id_rsa",
        #     remote_bind_address=('127.0.0.1', 27017),  # 
        # )
        # server.start()
        # client = MongoClient("127.0.0.1", server.local_bind_port)
        # print(server.local_bind_port)
        client = MongoClient("127.0.0.1", 27017)
        db = client["weixin"]
        self.table = db["source"]
    

    def response(self, flow):
        global  token
        url = flow.request.url
        biz_obj = {
            "企业全称": "full_name",
            "企业名称": "full_name",
            "机构全称": "full_name",
            "机构名称": "full_name",
            "认证时间于": "veify_time",
            "工商执照注册号/统一社会信用代码": "gs_credict_code",
            "工商执照注册号": "gs_credict_code",
            "组织机构代码/统一社会信用代码": "zz_credict_code",
            "经营范围(一般经营范围)": "work_range_common",
            "经营范围(前置许可经营范围)" :"work_range_front_premit",
            "企业类型": "company_classify",
            "主体": "company_classify",
            "机构类型": "company_classify",
            "企业成立日期": "company_create_date",
            "企业营业期限": "company_expire_date",
            "机构成立日期": "company_create_date",
            "机构有效期" : "company_expire_date",
            "名称记录" :  "name_record",
            "该帐号部分功能由以下服务商提供": "server_provider"

        }
        # print(flow.response.content.decode("utf-8"))
        if  re.match("https://mp.weixin.qq.com/mp/getverifyinfo?", url):  #企业验证主体
            query = flow.request.url.split("?")[-1]
            query = dict( parse_qsl(query) )
            __biz   = query.get("__biz")
            content = flow.response.content.decode("utf-8")
            re.search("认证时间于", content)
            soup = BeautifulSoup(content, features="html.parser")
            items = soup.find_all("li", "verify_item")
            info_filed = "info."
            infos = { 
                "info": {

                }
            }
            server_provider = re.search("thrid_list[\s\=\[]*([\s\,\"\u4e00-\u9fa5\(\)]+)",content)
            if server_provider and server_provider.group(1):
                server_provider = server_provider.group(1)
                # server_provider = server_provider.replace("\s\S","")
                server_provider = re.sub("[\s\"]","", server_provider)
                server_provider = server_provider
            else:
                server_provider = ""
            for item in items:    
                temp_key = item.find(class_= "verify_item_title")
                if temp_key:
                    string = temp_key.string.strip()
                    key = biz_obj.get(string)
                    if key:
                        temp_val = item.find(class_= "verify_item_desc")
                        if temp_val:
                            val = temp_val.string.strip()
                            #格式化时间字符串为时间
                            if key == "server_provider":
                               val = server_provider
                            if key == "company_create_date" or key =="company_expire_date":
                                try:
                                    val = datetime.strptime(val,"%Y年%m月%d日")
                                    val = val.timestamp()
                                except Exception as e:
                                    continue
                                
                                val = int(val*1000)
                        else:
                            val = None   
                            
                        infos["info"][key] = val
            self.table.update_one({"__biz": __biz}, {"$set": infos}, upsert=True)

        if  re.match("https://mp.weixin.qq.com/mp/profile_ext?", url):
            query = flow.request.url.split("?")[-1]
            query = dict( parse_qsl(query) )
            appmsg_token = query.get("appmsg_token")
            __biz   = query.get("__biz")
            if appmsg_token:
                self.appmsg_token =appmsg_token
            if __biz:
                self.__biz = __biz
            new_headers = dict(flow.request.headers)
            cookie = new_headers.get("Cookie")
            if cookie:
                cookie = cookie.replace(" ","")
            if query.get("appmsg_token"):     #抓取此地址的cookie 参数可以更具体点
                self.cookie = cookie
                self.new_headers["Cookie"] = cookie
                cookie = cookie.replace(";","&")
                # cookie =  my_parse_qsl(cookie)
                res = re.search("(?<=wap_sid2=)[0-9a-zA-Z=+]*\&*?",cookie)
                if res:
                    # wap_sid2 = cookie.get("wap_sid2")
                    wap_sid2 = res.group()
                    print("wap_sid2222222222")
                    print(wap_sid2)
                    print(url)
                    self.wap_sid2 = wap_sid2
                    self.new_headers.update({
                        "wap_sid2": self.wap_sid2
                    })

            soup = BeautifulSoup(flow.response.content)   #解析公众号名字
            nickName = soup.find(id='nickname')
            if nickName:
                self.nickName = nickName
            if  self.cookie and self.wap_sid2 and query.get("appmsg_token"):
                """
                    action=urlcheck
                    action=getmsg
                """
                self.new_headers.update({
                        "appmsg_token": self.appmsg_token,
                        "__biz": self.__biz,
                    })
                if self.nickName and self.appmsg_token:
                    self.nickName = self.nickName.get_text().strip()
                    self.new_headers.update({"NickName": self.nickName,  "updateAt":datetime.utcnow()})
                    self.table.update_one({"__biz": self.__biz}, {"$set": self.new_headers}, upsert=True)
                    self.new_headers = dict()
                    self.cookie = None
                    self.wap_sid2 = None
                    if to_update_list and self.nickName and self.count<1:
                        global Timer
                        Timer(1, update_list_func, (self.nickName,) ).start()
                    

                    self.nickName = None
                    # self.count = self.count +1  and self.count<1:
                    if self.count == 2:
                        self.count = 0


    def request(self,  flow):
        # print(flow)
        pass

    def requestheaders(self, flow):
        pass

    def http_connect(self, flow):
        pass



# from  mitmproxy.tools import dump
# print(tools.dump)
addons = [
    FetchSourceParam()
]
