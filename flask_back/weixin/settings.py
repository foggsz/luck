# -*- coding: utf-8 -*-

# Scrapy settings for weixin project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'weixin'

SPIDER_MODULES = ['weixin.spiders']
NEWSPIDER_MODULE = 'weixin.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
from  weixin.tool import USER_AGENT
USER_AGENT = USER_AGENT    #配置随机默认代理头

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8
# CLOSESPIDER_ERRORCOUNT  = 1
# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See alsDeo autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     # 'Referer': 'http://www.baidu.com',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'User-Agent': USER_AGENT,
#     'Connection': 'Keep-Alive',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'en-US,*'
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'weixin.middlewares.WeixinSpiderMiddleware': 543,
# }
# Retry many times since proxies often fail
RETRY_TIMES = 1
# # Retry on most error codes since proxies fail for different reasons
# RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'weixin.middlewares.WeixinDownloaderMiddleware': 543,
    # 'weixin.middlewares.WeixinSpiderMiddleware': 2,
    # "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware":100
    # 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110

}
# PROXY_LIST = '/path/to/proxy/list.txt'
# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': 500,
# #    'scrapy_jsonrpc.webservice.WebService': 500,  #网络服务 scrapy-jsonrpc
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#媒体管道 
ITEM_PIPELINES = {
    # 'scrapy.pipelines.images.ImagesPipeline': 1,   #默认图片管道
    # 'scrapy.pipelines.files.FilesPipeline': 1 ,     #默认文件管道
    'weixin.pipelines.MyImagesPipeline': 100,
    'weixin.pipelines.WeixinPipeline': 300

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

#mongo配置
MONGO_URL = "mongodb://localhost:27017/"
MONGO_DB_NAME = "weixin"
# LOG_ENABLED = False
# LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'
# LOG_FILE = None
# LOG_STDOUT = False

FEED_EXPORT_ENCODING = 'utf-8'

#收集器,存储数据保存在内存里，在当前某个爬虫内部通用
STATS_CLASS = 'scrapy.statscollectors.MemoryStatsCollector'


#webservice,爬取过程中检测
# JSONRPC_ENABLED=True 
# JSONRPC_LOGFILE=None 
# JSONRPC_PORT=[6080, 7030] 
# JSONRPC_HOST='127.0.0.1'


FILES_STORE = 'files'    #文件存储路径   官方支持Amazon S3 storage Google Cloud Storage
IMAGES_STORE = 'upload'   #图片存储路径
# IMAGES_URLS_FIELD = 'field_name_for_your_images_urls'   #设置媒体字段名
# IMAGES_RESULT_FIELD = 'field_name_for_your_processed_images'
# FILES_URLS_FIELD = 'field_name_for_your_files_urls'
# FILES_RESULT_FIELD = 'field_name_for_your_processed_files'
# FILES_EXPIRES = None      #避免下载最近120天以内的图片
# IMAGES_EXPIRES = None     #避免下载最近120天以内的图片
IMAGES_THUMBS = {       #指定缩略图大小和大图大小
    'small': (50, 50),
    'big': (270, 270),
}
MEDIA_ALLOW_REDIRECTS = True  #允许媒体重定向