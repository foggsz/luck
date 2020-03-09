from flask import session
import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from pydispatch import dispatcher
from scrapy  import signals
from app.main import socketio
import os
from multiprocessing import Process, Queue
import asyncio
import sys
from json import loads, dumps
from weixin.spiders.wx import mysignal, my_signals
from bson.json_util import  dumps
from datetime import datetime, timedelta
from time import perf_counter
from app.models import SpiderLogs, ExpireLogs

configure_logging()
kws = {
    "keyword":"河南",                         # keyword 组织名称或ID
    "condition":"detail",                    #list代表列表页   detail代表详情页 
                                            #isLoadImage  是否开启图片下载      
}
def item_passed(item, spider):   # 入库数据通知前端
    spider_name = spider.name
    item = loads( dumps(item))
    filter_keys = ['title', 'author', 'pub_time', 'biz_id', 'org_name', 'org_create_date', 'register_founds', 'unite_credict_code','org_classify','law_men', 
    'register_organ' , 'org_founds', 'register_status', 'gsl_name', "net_address", 'detail_url', 'category' , 'updateAt', 'region']
    item = dict([ (key, val) for key,val in item.items() if key in filter_keys ])
    names = {
        "gsl": "gsl_messag",
        "wx": "wx_message",
        "society": "society_message"
    }
    if spider_name in names.keys():
        message_name = names.get(spider_name)
        socketio.emit(message_name, item)

startTime = None
def spider_opened(spider):
    global startTime
    startTime = perf_counter()
 
    
def spider_closed(spider, reason):
    endTime = perf_counter()
    try:
        duration = int(endTime - startTime)
    except Exception as e:
        duration = 0

    close_data={
        "reason":reason
    }
    status = "success" if "finished" in reason else "fail"
    socketio.emit("closed", close_data)
    keyword = reason.split(":") [0]
    if keyword!="finished":
        insertData = {
            "info": reason,
            "duration":duration,
            "status": status,
            "keyword": keyword
        }
        SpiderLogs(**insertData).save()

def my_record(spider, **kws):
    kws.pop("sender")
    kws.pop("signal")
    kws.update({
        "classify": "biz",
        "createAt": datetime.utcnow()
    })
    ExpireLogs.objects(biz_id=kws.get("biz_id")).update_one(**kws,upsert=True)


def my_record_success(spider, **kws):
    # kws.pop("sender")
    # kws.pop("signal")
    ExpireLogs.objects(biz_id=kws.get("biz_id")).update(**{"status": "success"})

def my_error(spider, reason):
    endTime = perf_counter()
    try:
        duration = int( endTime - startTime )
    except Exception as e:
        duration = 0

    close_data={
        "reason":reason
    }
    socketio.emit("fail", close_data)
    keyword = reason.split("，") [0]
    insertData = {
        "info": reason,
        "duration":duration,
        "status": "fail",
        "keyword": keyword
    }
        
    SpiderLogs(**insertData).save()

def my_finished(spider, reason):
    endTime = perf_counter()
    try:
        duration = int(endTime - startTime)
    except Exception as e:
        duration = 0

    close_data={
        "reason":reason
    }
    status = "success" if "finished" in reason else "fail"
    socketio.emit("closed", close_data)
    keyword = reason.split(":") [0]
    if keyword!="finished":
        insertData = {
            "info": reason,
            "duration":duration,
            "status": status,
            "keyword": keyword
        }
        SpiderLogs(**insertData).save()
    else:
        if spider.name == "gsl":
            insertData = {
                "info":  "爬虫" + spider.name + "运行完成",
                "duration":duration,
                "status": status,
                "keyword": "爬虫" + spider.name + "运行完成",
            }
            SpiderLogs(**insertData).save()


def run_spider(*args, **kw):  #启动爬虫
    mysignal.connect(my_error, signal=my_signals.get("error"))
    mysignal.connect(my_finished, signal=my_signals.get("finished"))
    mysignal.connect(my_record, signal=my_signals.get("record"))
    mysignal.connect(my_record_success, signal=my_signals.get("record_success"))
    dispatcher.connect(item_passed, signal=signals.item_passed)
    dispatcher.connect(spider_opened, signal=signals.spider_opened)
    dispatcher.connect(spider_closed, signal=signals.spider_closed)
    runner = CrawlerRunner(settings=get_project_settings())
    spiderName = kw.get("spiderName", "wx")
    runner.crawl(spiderName,  **kw)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) == 2:
        kws = loads(argv[-1])
        run_spider(**kws)
                            