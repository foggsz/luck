# -*- coding: utf-8 -*-



import scrapy
import logging
import  math
import pymongo
from scrapy.utils.log import configure_logging
from weixin.settings  import  MONGO_URL
from weixin.settings  import  MONGO_DB_NAME
from weixin.items import doubanItems
from weixin.loader  import SociteyLoader
import time
import re
from twisted.python import log
from scrapy.exceptions  import  CloseSpider
import json
from scrapy import Selector
from scrapy import FormRequest
from weixin.tool import USER_AGENT
from weixin.items import societyItems

tableKeys = {
    "登记管理机关": "register_organ",
    "业务主管单位":  "org_listener",
    "法定代表人":  "law_men",
    "成立登记日期": "org_create_date",
    "注册资金": "register_founds",
    "登记状态": "register_status",
    "网址":  "org_url",
    "联系电话":  "org_phone",
    "登记证号":  "register_code",
    "社会组织类型": "org_classify",
    "住所":  "org_address",
    "业务范围": "work_range",
    "证书有效期": "org_cert_expire"
}

class SocietySpider(scrapy.Spider):
    name = 'society'
    allowed_domains = ['chinanpo.gov.cn']
    start_urls = ['http://www.chinanpo.gov.cn/search/orgcx.html']
    custom_settings = {
        "ITEM_PIPELINES":{
            "weixin.libs.mongopipe.SocietyMongoPipeline":300,
        },
        "CONCURRENT_REQUESTS":24,
        "CONCURRENT_REQUESTS_PER_DOMAIN ":24,
        "CONCURRENT_REQUESTS_PER_IP ": 24,
        "DOWNLOAD_DELAY": 0,
        "COOKIES_ENABLED": False,
    }
    handle_httpstatus_list = [301, 302]
    def __init__(self, *args, goto_page=1, page_size = 20, **kws):
        extra = kws.get("extra") or [] #其他条件
        self.allLoad = True if "allLoad" in extra else False
        self.goto_page = goto_page
        self.page_size = page_size
        types = {'mzb':1, 'df': 2,}
        typeNames = {'mzb':"民政部登记", 'df': "地方登记",}
        self.org_type = kws.get('org_type', "mzb")
        if self.org_type  not in types:
            return 
        self.typeName = typeNames.get(self.org_type)
        self.tabIndex = types.get(self.org_type)
        self.client = pymongo.MongoClient(MONGO_URL)
        self.db  = self.client[MONGO_DB_NAME]
        self.society = self.db["society"]
        self.lastest_one = None
        self.total_count = None
        self.total_page = None
        self.mzb_detail_url = "http://www.chinanpo.gov.cn/search/vieworg.html"
        self.df_detail_url = "http://www.chinanpo.gov.cn/search/poporg.html"   
        self.query = {
            "status": "-1",   #全部
            "regNum": "-1",
            "page_flag":  "true",
            "goto_page": "{0}".format(self.goto_page),
            "page_size": "{0}".format(self.page_size),
            "tabIndex":  "{0}".format(self.tabIndex),   #1是民政部  2是地方
        }
        self.parttern = {
            "org_name": re.compile("[\u4e00-\u9fa5\(\)\（\）\【\】\[\]]+"),
            "unite_credict_code": re.compile("[0-9a-zA-Z]+"),
        }
        self.headers = {
                "Origin": "http://www.chinanpo.gov.cn",
                "Referer": "http://www.chinanpo.gov.cn/search/orgcx.html",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        }

    def start_requests(self,):
        self.lastest_one = self.get_lastone()
        for url in self.start_urls:
            if self.total_page is None:
                yield scrapy.FormRequest(url= url, formdata = self.query, method="POST", callback=self.get_total, headers=self.headers)   #获得总数
            # yield scrapy.FormRequest(url= url, formdata = self.query, method="POST", callback=self.parse)

    def get_total(self, response):
        s = Selector(response=response)
        x = s.css('.bscx-div-8').extract_first()
        total_count = s.css('.bscx-div-8 input[name=total_count]::attr(value)').extract_first()
        if total_count:
            self.total_count =  int(total_count)
            self.total_page =  math.ceil(self.total_count/self.page_size)
            self.query.update({
                "total_count": str(self.total_count)
            })
            yield scrapy.FormRequest(url= response.url, formdata = self.query, method="POST", callback=self.parse, dont_filter=True, headers=self.headers)  #获得总数 
        else:
            raise CloseSpider(reason="全国社会组织网:获取总数出错，程序停止")

    def get_lastone(self,):
        lastest_one = self.society.find({"org_type":  self.org_type}).sort("org_create_date", -1).limit(1)
        lastest_one = list(lastest_one)
        if  len(lastest_one) ==0:
            lastest_one = {}
        else:
            lastest_one = lastest_one[0]
        return lastest_one

    def parse(self, response):
        s = Selector(response=response)
        l = SociteyLoader(item=societyItems())
        if self.org_type == "mzb":
            for item in s.css(".table-1  tr  td[align=left]  a::attr(href)").extract():
                try:
                    org_id = re.search('[0-9]+',item).group()
                except Exception  as e:
                    continue
                    
                else:
                    l.add_value("org_id", org_id)
                    if not self.allLoad: #不需要全部下载才进行最新日期抓取，针对更新，针对重新采集
                        if self.lastest_one.get("org_id") and self.lastest_one.get("org_id") == org_id: 
                            self.client.close()
                            raise CloseSpider(reason="{0}:更新完毕:finished".format(self.typeName))
                    yield scrapy.FormRequest(url= self.mzb_detail_url, formdata = {'orgId': org_id}, method="POST", callback=self.parseDetail, meta={"org_id": org_id}, dont_filter=True, headers=self.headers)
    
        elif self.org_type == "df":
            # with open("1.html", "a+") as f:
            #     x = s.css(".table-1  tr  td[align=left]  a::attr(href)").extract()
            #     f.write(x)
            for item in s.css(".table-1  tr  td[align=left]  a::attr(href)").extract():
                try:         
                    item = item.replace('"',"")
                    tempiu = re.search("\(([\s\S]*)\)", item).group(1).replace("'","")
                    tempiu = tempiu.split(",")
                except Exception  as e:
                    continue
                else:
                    l.add_value("i", tempiu[0])
                    l.add_value("u", tempiu[1])
                    if not self.allLoad: #不需要全部下载才进行最新日期抓取，针对更新，针对重新采集
                        if self.lastest_one.get("i") == tempiu[0] and self.lastest_one.get("u") == tempiu[1]: 
                            self.client.close()
                            raise CloseSpider(reason="{0}:更新完毕:finished".format(self.typeName))
                    tempUrl = "{0}?i={1}&u={2}".format(self.df_detail_url, tempiu[0], tempiu[1])
                    yield scrapy.FormRequest(url= tempUrl, method="POST", callback=self.parseDetail, meta={
                        "i": tempiu[0],
                        "u": tempiu[1],
                    }, dont_filter=True, headers=self.headers)
        
        url = response.url
        if self.goto_page <= self.total_page:
            self.goto_page = self.goto_page +1
            self.query.update({
                "goto_page":"{0}".format(self.goto_page) 
            })
            yield scrapy.FormRequest(url = url,  formdata = self.query, method="POST", callback=self.parse , dont_filter=True, headers=self.headers)
        else:
            self.client.close()
            raise CloseSpider(reason="{0}:收集完毕:finished".format(self.typeName))

    def filter(self, key, text=None, arr=None):
        try:
            if arr:
                if key == "org_name":
                    text = arr[0]
                elif key == "org_tag":
                    if len(arr) >= 3:
                        text = arr[1:-1]
                    else:
                        text = None
                elif key == "unite_credict_code":
                    parttern = self.parttern.get(key)    
                    text = re.search(parttern, arr[-1])
                    text  = text.group()
            else:
                parttern = self.parttern.get(key)    
                text = re.search(parttern, text)
                text = text.group()
        except Exception as e:
            return None
        else:
            return text 

    def parseDetail(self, response, ):  
        meta = response.request.meta
        s = Selector(response=response)
        res = response.body_as_unicode()
        l = SociteyLoader(item=societyItems(), response=response)
        title = s.css(".title_bg h3").extract_first()
        if title:
            temp_arr = re.findall("(?<=[a-zA-Z<>])*[\u4e00-\u9fa5\(\)\（\）\【\】\[\]]+[：0-9a-zA-Z]*",title)
            org_name = self.filter("org_name", arr=temp_arr)
            org_tag = self.filter("org_tag",  arr=temp_arr)
            unite_credict_code = self.filter("unite_credict_code", arr=temp_arr)
            l.add_value("org_name", org_name)
            l.add_value("org_tag", org_tag)
            l.add_value("unite_credict_code", unite_credict_code)
            l.add_value("org_type", self.org_type)
            if meta.get("org_id"):
                l.add_value("org_id", meta.get("org_id"))
            if meta.get("i"):
                l.add_value("i", meta.get("i"))
            if meta.get("u"):
                l.add_value("u", meta.get("u"))
            array  =  s.css("table.mar-top tr td::text").extract()

            for index, item in  enumerate(array, 0):
                item = re.sub('[\s：]+', "", item)
                if  item!="":
                    key =  tableKeys.get(item)
                    if key:
                        try: 
                            if key  == "org_address" or key == "work_range":  #colspan = 3
                                tmp_value = ''.join(array[index+1:index+4])
                            else:
                                tmp_value = array[index+1]   
                        except Exception as e:
                                break
                        else:
                            tmp_value = re.sub('[\s：]+', "", tmp_value)
                            l.add_value(key, tmp_value)  
            yield l.load_item()

        else:
            if meta.get("org_id"):
                self.logger.warning("组织ID{0}异常".format(meta.get("org_id")))
            elif meta.get("i") and meta.get("u"):
                self.logger.warning( "组织IDi={0},u={1}异常".format(meta.get("i"),meta.get("u")) )