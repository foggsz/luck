from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity
from w3lib.html import remove_tags, strip_html5_whitespace
import html
import re
from datetime  import datetime

class myLoder(ItemLoader):
    default_input_processor = MapCompose(remove_tags, strip_html5_whitespace)
    default_output_processor = TakeFirst()

def handle_img_urls(url):
    url  =  url.replace("", "")
    if url.startswith("//"):
        url =  "http:" +url
    if url.startswith("http"):
        return url
        
def contentFunc(url):
    return html.unescape(url)

class wxLoader(ItemLoader):
    default_output_processor = TakeFirst()
    time_in = MapCompose(lambda x: int(x)*1000)
    pub_time_in = MapCompose(lambda x: int(x)*1000)
    image_urls_in = MapCompose(handle_img_urls)
    image_urls_out = Identity()
    content_url_in = MapCompose(contentFunc)     


class wxDetailLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, strip_html5_whitespace)
    default_output_processor = TakeFirst()
    content_in = Identity()
    # pub_time_out = Identity()
    # list_id_out = Identity()
    # content_url_out = Identity()
    # content_url_out = MapCompose(contentFunc)
    # title_in = MapCompose(x)
    # time_in = MapCompose(lambda x: int(x)*1000)
    pub_time_in = MapCompose(lambda x: int(x))
    image_urls_in = MapCompose(handle_img_urls)
    image_urls_out = Identity()

def int_number(n):
    return int(n)

def NickName(text):
    text = re.search("[\u4e00-\u9fa5]+", text)
    text = text.group() if text else None
    return text
    
def unite_credict_code(text):
    text = re.search("[0-9A-Za-z]+", text)
    text = text.group() if text else None
    return text

def formt_date(text):
    temp = re.findall("[0-9-]+", text)
    if(len(temp) ==1):
        time = datetime.strptime(temp[0],"%Y-%m-%d")
        time = time.timestamp()
        time = int(time*1000)
        return time
    elif (len(temp) ==2):
        time_start = datetime.strptime(temp[0],"%Y-%m-%d")
        time_start = time_start.timestamp()
        time_start = int(time_start*1000)
        time_end = datetime.strptime(temp[1],"%Y-%m-%d")
        time_end = time_end.timestamp()
        time_end = int(time_end*1000)
        time = [time_start, time_end]
        return time

def covert_array(arr):
    if arr and type(arr) == list:
        return arr

class SociteyLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, strip_html5_whitespace)
    default_output_processor = TakeFirst()
    orgId_in = MapCompose(int_number)
    org_create_date_in = MapCompose(formt_date)
    org_cert_expire_in = MapCompose(formt_date)
    org_cert_expire_out = Identity()
    org_tag_in  = MapCompose(covert_array)
    org_tag_out = Identity()


def strtToTime(value):
    try:
        datetimeobj = datetime.strptime(value, "%Y-%m-%d")
        datetimeobj = datetimeobj.timestamp()
        datetimeobj = int(datetimeobj*1000)
    except Exception as e:
        return None
    else:
        return datetimeobj

def full_province(value):
    provinces = ['北京市','天津市', '上海市', '重庆市', '河北省', '山西省', '辽宁省', '吉林省', '黑龙江省', '江苏省', '浙江省', '安徽省', '福建省',
    '江西省','山东省','河南省', '湖北省' , '湖南省', '广东省', '海南省', '四川省', '贵州省', '云南省', '陕西省', '甘肃省', '青海省', '台湾省', '内蒙古自治区', '广西壮族自治区', '西藏自治区',
    '宁夏回族自治区', '新疆维吾尔自治区', '香港特别行政区', '澳门特别行政区']
    for p in provinces:
        if value in p:
            value = p
            break
    return [value]
class gslLoader(ItemLoader):
    default_input_processor = MapCompose(remove_tags, strip_html5_whitespace)
    default_output_processor = TakeFirst()
    pub_time_in = MapCompose(strtToTime)
    region_in = MapCompose(remove_tags, strip_html5_whitespace, full_province)
    region_out = Identity()