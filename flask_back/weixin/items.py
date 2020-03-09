# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags
class doubanItems(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field(  
    ) 
    act = scrapy.Field(
    )
    actLeader = scrapy.Field()
    stars = scrapy.Field()
    commentNum =scrapy.Field()
    intro = scrapy.Field()

class wxItems(scrapy.Item):    #公众号列表数据模型
    title = scrapy.Field()         #标题
    subName = scrapy.Field()       #简介
    content = scrapy.Field()       #内容
    article_type = scrapy.Field()  #文章类型
    author = scrapy.Field()        #作者
    comm_msg_info = scrapy.Field()  #一些公用信息
    source_url = scrapy.Field()    #源地址
    content_url = scrapy.Field()   #内容地址
    fileid   =  scrapy.Field()     #列表文章ID
    fakeid   =  scrapy.Field()     #公共消息主体编号
    cover  = scrapy.Field()        #封面地址
    biz_id = scrapy.Field()         #公众号ID
    org_name = scrapy.Field()         #组织号名称
    pub_time = scrapy.Field()      #发布时间
    image_urls = scrapy.Field()    #图片地址
    image_paths = scrapy.Field()    #图片路径

class wxDetailItems(scrapy.Item):    #公众号文章详情模型
    title = scrapy.Field()         #标题
    author = scrapy.Field()        #作者
    content = scrapy.Field()       #内容
    pub_time = scrapy.Field()      #发布时间
    list_id = scrapy.Field()       #列表Id
    biz_id = scrapy.Field()        #公众号ID
    content_url = scrapy.Field()   #去重
    image_urls = scrapy.Field()    #图片地址
    image_paths = scrapy.Field()    #图片路径


class  societyItems(scrapy.Item):
    org_name = scrapy.Field()     #组织名称
    unite_credict_code = scrapy.Field()  #统一社会组织代码
    register_organ = scrapy.Field()  #登记管理机关
    org_listener = scrapy.Field()   #业务主管机构
    law_men = scrapy.Field()           #法定代表人
    org_phone = scrapy.Field()          #联系电话
    register_founds = scrapy.Field()   #注册资金
    register_status = scrapy.Field()    #登记状态
    org_create_date = scrapy.Field()   #成立登记日期
    register_code = scrapy.Field()   #登记证号
    org_classify  = scrapy.Field()      #社会组织类型
    org_url = scrapy.Field()               #组织网址
    org_address = scrapy.Field()        #住所
    org_id =  scrapy.Field()           #组织ID  民政部登记有
    updateAt = scrapy.Field()          #更新时间
    org_type = scrapy.Field()              #登记类型
    i  = scrapy.Field()               #地方登记有
    u  = scrapy.Field()               #地方登记有
    org_cert_expire  = scrapy.Field()    #证书有效期
    work_range = scrapy.Field()     #业务范围
    org_tag  = scrapy.Field()      #组织标签
    region  = scrapy.Field()      #地区分布

class  gslItems(scrapy.Item):
    _id = scrapy.Field() 
    gsl_name = scrapy.Field()       #工商联名称
    gsl_sub = scrapy.Field()        #简介
    category = scrapy.Field()       #抓取的栏目
    title  = scrapy.Field()         #文章标题
    pub_time  = scrapy.Field()      #发布时间
    source  = scrapy.Field()        #文章来源
    summary =  scrapy.Field()       #文章简介
    content =  scrapy.Field()       #文章来源
    region = scrapy.Field()         #工商联所属地区
    net_address = scrapy.Field()     #网址
    detail_url = scrapy.Field()     #详情网址
    updateAt = scrapy.Field()     #更新日期
