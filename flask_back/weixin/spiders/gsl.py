# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from weixin.items  import gslItems
from weixin.loader import gslLoader
from app.models import  GSL
import re
from urllib.parse import urljoin
import time
from scrapy import Selector
from scrapy.exceptions  import CloseSpider
from json import loads
import logging
def process_value(value):
    print(value)
    return value


class GslSpider(CrawlSpider):
    name = 'gsl'
    allowed_domains = ['acfic.org.cn']
    # start_urls = ['http://www.acfic.org.cn']
    start_urls =  ["http://www.acfic.org.cn/gdgsl_362/sx/sxgslgz/index_1.html"]
    rules = (
        Rule(LinkExtractor( allow=r'gdgsl_362\/[a-z]+\/$' , tags=('a', 'area'), attrs=("href", ) ), callback='parse_item_brige',  follow=True),    #此处处理地方JS跳转  /html/body/div[3]/div[2]/div[2]/div[2]/div[2]/div/div/p[3]/a
        Rule(LinkExtractor( allow=r'gdgsl_362\/[a-z]+\/[a-z]+\/$' ,), callback='parse_item',  follow=True,),    #真实处理跳转 index\_[0-9\.html\/]+

    )
    
    # handle_httpstatus_list = [301, 302]
    custom_settings = {
        "ITEM_PIPELINES":{
            "weixin.libs.mongopipe.GSLMongoPipeline":300,
        },
        "DOWNLOADER_MIDDLEWARES": {
            "weixin.libs.downloader.GSLDownLoader":300,
        },
        "DOWNLOAD_DELAY": 0.2,
        "CONCURRENT_REQUESTS":16,
        "CONCURRENT_REQUESTS_PER_DOMAIN ":16,
        "COOKIES_ENABLED": False,
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
    def __init__(self,*args, **kw): 
        self.last_one = {}
        self.start_urls = kw.get("start_urls")  or  self.start_urls 
        extra = kw.get("extra", []) #其他条件
        self.all_load =  True  if "allLoad" in extra  else False
        if kw.get("rules"):
            self.rules =  self.rules + kw.get("rules")
        self.find_last_one()
        super().__init__(*args, **kw)


    def parse_start_url(self, response):  #处理首页
        return []



    def find_last_one(self, ):
        try:
            res = GSL.objects.order_by("-pub_time").limit(1).to_json()
        except Exception as e:
            pass
        else:
            res = loads(res)
            if res:
                self.last_one = res[0]

    def parse_item_brige(self, response):
        address = response.css("script::text").extract_first()
        if address:
            res = re.search("\({1,}'*([\.\/a-z]+)",address)
            if res:
                address = res.group(1)
                return  response.follow(address+'/index.html')



    def parse_item(self, response):
        body = response.body_as_unicode()
        # l = gslLoader(item=gslItems(), response=response)
        # title = l.add_css("region", "title")
        # gsl_name  =  l.add_css("gsl_name", "div.TRS_Editor font")
        # net_address = l.add_css("net_address", "div.TRS_Editor p a")
        # region =  l.add_css("category", "div.location a.CurrChnlCls:nth-child(4)")
        # l = l.load_item()
        region = response.css("title::text").extract_first()
        gsl_name = response.css("div.TRS_Editor font::text").extract_first()
        net_address =response.css("div.TRS_Editor p a::text").extract_first()
        category =  response.css("div.location a:nth-child(4)::attr(title)").extract_first()
        for li in response.css("div.gdgslListItem li"):
            l = gslLoader(item=gslItems(), response=response)   
            l.add_value("region", region)
            l.add_value("gsl_name", gsl_name)
            l.add_value("net_address", net_address)
            l.add_value("category", category)
            title = li.css("a:nth-child(2)").extract_first()
            detail_url = li.css("a:nth-child(2)::attr(href)").extract_first()
            pub_time =  li.css("span::text").extract_first().strip()
            if detail_url:
                detail_url  =  urljoin(response.url, detail_url)       
                if not self.all_load  and detail_url == self.last_one.get("detail_url") :
                    raise CloseSpider(reason="{0}:列表页更新完成:finished".format("所有省级单位"))
            l.add_value("pub_time", pub_time)      
            l.add_value("title", title)
            l.add_value("detail_url", detail_url)
            l = l.load_item()
            yield l

        #寻找下一页
        countPage  = re.search("var\s+countPage\s+\=\s+([0-9]+)", body) 
        if countPage:
            countPage = countPage.group(1) 
            countPage = int(countPage)
            if countPage >1:
                currentPage = response.meta.get("currentPage", 1)
                currentPage = currentPage +1
                yield  response.follow( url = "index_{0}.html".format(currentPage), meta={ "currentPage": currentPage }, callback= self.parse_item, dont_filter=True)
                     

