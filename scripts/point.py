from bs4 import BeautifulSoup
import os
import re
import time
from subprocess import Popen
device = ''
args = {
    "搜索": "search_btn",
    "通讯录": "telList_btn",
    "公众号" : "gzh_btn",
    "联系人" : "link_men", 
    "android.support.v7.widget.LinearLayoutCompat": "gzhDetail_btn",
    re.compile(r"com.tencent.mm:id\/a6e|com.tencent.mm:id\/zx"): "swipe0",
    "com.tencent.mm:id/avt": "allMessage_btn",
    "android.widget.EditText":  "edit",   #编辑键位
    "发送":  "send",  #发送键位
    re.compile(r"com.tencent.mm:id\/mq|com.tencent.mm:id\/mr"): "nowUrl",   #当前需要点击的UR;
    "文件传输助手": "help",
    re.compile(r"继续|QQ浏览器X5内核提供技术支持"):  "alert" , #安全警告,或者是关闭

}
file_args = {
    "search_btn": "index.xml",
    "telList_btn": "index.xml",
    "gzh_btn" :  "page1.xml",
    "gzhDetail_btn": "page2.xml",
    "allMessage_btn":  "page3.xml",
    "swipe0": "swipe0.xml",
    "edit":  "page4.xml",
    "send":  "page5.xml",  #发送键位
    "nowUrl": "page6.xml",
    "help":   "page7.xml",
    "alert":  "page8.xml",
    
}

points = {
    "map": []   #公众号列表地图
}

def filter_key(key):
    keys = []
    for item in points["map"]:
        temp_keys =  list(item.keys())
        keys = keys +temp_keys
    if key in keys:
        return False
    return True

def alert(soup):
    find  =  soup.find(attrs= {"text": "继续" })
    limit = soup.find(attrs= {"text": "QQ浏览器X5内核提供技术支持"})
    if find:
        try:
            find = find.get("bounds")
            index = find.index("]")
        except Exception as e:
            return None
        else:
            return find[1:index].split(",")
    else:
        if limit:
            return 'limit'
        return None

def copy(name):
    order_0 = "adb {0} shell uiautomator dump /data/local/tmp/{1}".format(device, name)
    order_1 = "adb {0} pull /data/local/tmp/{1}   ./".format(device, name)
    try:
        pipe = Popen(order_0, shell=True)
        pipe.wait()
        pipe = Popen(order_1, shell=True)
        pipe.wait()
    except Exception as e:
        print(e)
        
total = 0
def find_swipe(res, args, findName=None):
    global total
    if args  == "swipe0":
        while True:
            pipe = Popen("adb {0} shell  uiautomator dump /data/local/tmp/{1}_temp.xml".format(device, args), shell=True)
            pipe.wait()
            pipe = Popen( "adb {0} pull  /data/local/tmp/{1}_temp.xml   ./".format(device, args),  shell=True)
            pipe.wait()
            with open("{0}_temp.xml".format(args)) as f:
                data = f.read()
                soup = BeautifulSoup(data, 'xml')
                res_temp = soup.find(attrs= {"resource-id": "com.tencent.mm:id/azu" })
                gzh = soup.find_all(attrs= {"resource-id": "com.tencent.mm:id/a6e" })
                if gzh:
                    temp_obj = {}
                    for item in gzh:
                        if item.get("text") and item.get("bounds"):
                            temp_index = item.get("bounds")
                            temp_index = temp_index.index("]")
                            temp_point = item.get("bounds")[1:temp_index].split(",")
                            if filter_key(item.get("text")):
                                temp_obj.update({
                                    item.get("text"): temp_point,
                                })
                            if item.get("text") == findName:
                                return temp_point
                    if temp_obj:
                        points["map"].append(temp_obj)

                if res_temp:
                    try:
                        res_temp = res_temp.get("text")
                        res_temp = re.search("[0-9]+", res_temp).group()
                        if res_temp:
                            total = total +1 
                            return total , int(res_temp)
                            # return int(res_temp)
                        raise("无法获取总数")
                    except  Exception as e:
                        raise

            end = res[0].get("bounds")
            start = res[-1].get("bounds")
            try:
                start  = start[1:-1].split("][")[0]
                end = end[1:-1].split("][")[-1]
                start = start.split(",")
                end = end.split(",")
                end[-1] = int(end[-1])-1
                points["map"][total].update({
                    "swipe": [int(start[0]), int(start[1]), int(end[0]), int(end[1]) ]
                })
                pipe = Popen( "adb {0} shell input swipe  {1} {2} {3}  {4} 1000".format(device, start[0], start[1], end[0], end[1]), shell= True )
                pipe.wait()
                total  = total + 1
            except Exception as e:
                print(e)

def getNow_url(res):
    res = res[-1]
    res = res.get("bounds")
    index = res.index("]")
    start = res[1:index].split(",")
    end = res[index+2:-1].split(",")
    x = int( ( int(start[0]) + int(end[0]) )/2 )
    y = int(start[1])+55
    print(x,y)
    return [x, y]

def find(data, keyword, arg="", findName=None):
    soup = BeautifulSoup(data, 'xml') 
    if(arg == "alert"):
        return alert(soup)
    res = soup.find(attrs= {"content-desc": keyword})  or  soup.find(attrs= {"text": keyword}) or  soup.find(attrs= {"class": keyword}) or soup.find_all( attrs= {"resource-id":
    keyword})
    if res:
        if "swipe" in arg or findName:
            res = find_swipe(res, arg, findName=findName)
            return res
        if arg == "nowUrl":
            return getNow_url(res)

        else:
            if arg == "allMessage_btn":
                res = res[0]
            res = res.get("bounds")
            try:
                index = res.index("]")
            except Exception as e:
                return None
            else:
                return res[1:index].split(",")
    else:
        if arg == "allMessage_btn":
           pipe = Popen("adb {0} shell input swipe  50  1279  50  0  1000 ".format(device), shell=True)
           pipe.wait()
           return get_point(arg)           
    return None

    

def open_file(filename):
    while True:
        if os.path.exists(filename):
            if filename not in ["index.xml", "page1.xml", "page2.xml"]:
                copy(filename)
                time.sleep(1)
            try:
                f = open(filename)
                data = f.read()

            except Exception as e:
                print(e)
                return None
            else:
                return data
        else:
            copy(filename)
            time.sleep(1)

def get_point(arg, findName=None, toDevice=None):
    global device
    if toDevice:
        device = toDevice
    filename = file_args.get(arg)
    if arg == "allMessage_btn":
        pipe = Popen("adb shell {0} input swipe  50  1279  50  0  1000 ", shell=True).format(device)
        pipe.wait()

    data = open_file(filename)
    if data:
        for key, val in args.items():
            if  val == arg:
                temp = find(data, key, arg, findName=findName)
                if temp:
                    points.update({
                        val:temp
                    })
                    return temp

    # else:
    #     raise ValueError("得不到坐标文件数据,请确认传入关键词。或者文件名")        

