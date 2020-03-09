# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.utils.log import configure_logging
from weixin.items import doubanItems
from weixin.loader  import myLoder
import time
from twisted.python import log
from scrapy.exceptions  import  CloseSpider
items  = doubanItems()
class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']
    custom_settings = {
        'ITEM_PIPELINES': {
            'weixin.pipelines.WeixinPipeline': 300,
        },
        'LOG_FILE': '../DoubanSpider_DEBUG.log',
        'LOG_LEVEL': 'INFO',
    }
    def start_requests(self,):
        self.crawler.stats.set_value('s',9999) 
        raise CloseSpider(reason="sddsdssdds")
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)
    def parse(self, response):
        """ This function parses a sample response. Some contracts are mingled
        with this docstring.
        @url https://movie.douban.com/top250/sdsdsdsdsdssdds
        @returns requests 0 0
        @scrapes name
        """
        # self.logger.info("sdssdsdd")
        for item in response.css("ol.grid_view li"):
            l = myLoder(item=doubanItems(), selector=item)
            l.add_css('name','span.title::text')
            l.add_css('act',  "div.bd p::text")
            self.crawler.stats.set_value("s",11)
            res =  l.load_item()
            print(res)
            yield res


      
        
