from selenium  import webdriver
from scrapy.http import HtmlResponse
import re
import time

class Chorme_agent(object):

    def __init__(self):
        pass

    def process_request(self, request, spider):

        if not re.match("^https://mp.weixin.qq.com", request.url):
            return None

        self.driver = webdriver.Chrome("/Users/zhixi/chromedriver")
        self.driver.get("https://admin.dazhongyueche.com/taxi")
        time.sleep(15)
        self.driver.get(request.url)
        self.driver.add_cookie({"name":"wap_sid2",  "value":"COLVoZYIElxOZWpud0NiSUQ0eXpBSkh3WUFSTmwzUTI4c050MWpINU1sS24tNkJjOTZNc2NoeS04T0MySy0wZTYyLVZmdjRGZUtwRTFvcXVFcFZtZkl2bndFa3dXZEFEQUFBfjC5+8jdBTgNQJVO"})
        self.driver.refresh()
        body = self.driver.page_source
        response =  HtmlResponse(url = self.driver.current_url, body=body, encoding='utf-8')
        self.driver.close()
        return response
        