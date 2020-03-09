from selenium  import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import quote
import time
from json import loads
from  point import get_point, points
from subprocess import PIPE, Popen
import re
import shlex
import sys
argv = sys.argv

device = None
driver = webdriver.Chrome("/Users/pingguo1zhixi/fog/chromedriver")
js_cookies_get =  """
        function getCookie(name)
        {
        var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
        if(arr=document.cookie.match(reg))
        return unescape(arr[2]);
        else
        return null;
        }
        let urls = getCookie(arguments[0]);
        if(urls) {
            if (arguments[1]) {
                return urls
            }
            return JSON.parse(urls);
        }else{
            return null;
        }
    """

js_cookies_set =  """
        function setCookie(key, value)
        {
            document.cookie = key+"="+value
        }
        setCookie(arguments[0], arguments[1])
    """  

def getDevices(): #所有的设备
    step0 = "adb devices"
    pipe = Popen(step0, shell=True, stdout=PIPE)
    pipe.wait()
    devices = pipe.stdout.readlines()
    del devices[0]
    for i in range(len(devices)):
        devices[i] =  devices[i].decode("utf-8")
        if devices[i] == "\n":
            del devices[i]
            continue 
        devices[i] =  " -s   " + re.sub("[\s\t]*(device)*", "", devices[i])
    return devices   

def start(): #启动微信
    step0 = "adb {0} shell am start -n  com.tencent.mm/.ui.LauncherUI ".format(device)
    pipe = Popen(step0, shell=True)
    pipe.wait()
    time.sleep(10)
    help_x, help_y = get_point("help", toDevice=device)
    step1 = "adb {0} shell input tap  {1} {2}".format(device, help_x, help_y)
    pipe = Popen(step1, shell=True)
    pipe.wait()

def step(url):  #每一步
    adb_start = "adb {0} shell  ".format(device)
    adb_start = shlex.split(adb_start)
    url = str(url)
    url = '\''+ url + '\''
    edit_x, edit_y = get_point("edit", toDevice=device)
    pipe = Popen(adb_start, stdin=PIPE, stdout=PIPE)
    step0 = """
        input tap {0} {1}
        input text {2}
        input keyevent 111
        exit
    """.format(edit_x, edit_y, url)
    step0 = bytes(step0, encoding="utf-8")
    pipe.communicate(input=step0)
    send_x, send_y = get_point("send", toDevice=device)
    setp1 = "adb {0} shell input tap {1} {2}".format(device, send_x, send_y)
    pipe = Popen(setp1, shell=True)
    pipe.wait()

    nowUrl_x, nowUrl_y = get_point("nowUrl", toDevice=device)
    setp2 = "adb {0} shell input tap {1} {2} ".format(device, nowUrl_x, nowUrl_y)
    pipe = Popen(setp2, shell=True)
    pipe.wait()
    time.sleep(8)

    temp_alert = get_point("alert", toDevice=device)  #安全警告还是  被限制
    if temp_alert:
        if temp_alert == "limit":
            raise ValueError("limit") 
        else:
            alert_x, alert_y = temp_alert
            setp3 = "adb {0} shell input tap {1} {2} ".format(device, alert_x, alert_y)
            pipe = Popen(setp3, shell=True)
            pipe.wait()
            time.sleep(5)
    setp4 = "adb {0} shell input keyevent 4".format(device)
    pipe = Popen(setp4, shell=True)
    pipe.wait()

def tryNext(devices, limit_id=None):
    try:
        del devices[0]
    except  IndexError  as e:  #所有设备用完
        print("所有手机已经用完")
        return
    else:
        print('开始换号')
        if limit_id:
            driver.execute_script(js_cookies_set, "sourceId", limit_id)
            return webDriver(devices)
        return 

def webDriver(devices):
    global device
    try:
        device = devices[0]
    except  IndexError  as e:  #所有设备用完
        print("所有手机已经用完")
        return 
    start()    #启动微信
    while True:
        driver.find_elements_by_css_selector("#app > div > div.main-container > section > div > div > button")[0].click()
        time.sleep(4)
            
        urls = driver.execute_script(js_cookies_get, "urls")
        finish = driver.execute_script(js_cookies_get, "finish", "noJSON")
        if finish:
            # driver.close()
            if finish == 'over':
                pipe = Popen("adb {0} shell  am  force-stop  com.tencent.mm".format(device), shell=True)
                pipe.wait()
                break
            else:  #账号被限制
                return tryNext(devices)
                 
        if urls:
            for item in urls:
                temp_url =  item.get("url")
                try:
                    step(temp_url) 
                except Exception as e:
                    print(e)
                    return tryNext(devices, limit_id = item["_id"]["$oid"])

        
def run():
    devices = getDevices()   #所有手机设备
    # base_url = "https://wx.hnzhixi.com/adb"
    base_url = "http://localhost:9528/adb"
    driver.get(base_url) 
    username_e = driver.find_elements_by_xpath('//*[@id="app"]/div/form/div[1]/div/div/input')[0]
    ActionChains(driver).double_click(username_e).send_keys("script_admin").perform()
    time.sleep(1)
    driver.find_elements_by_css_selector("#app > div > form > div:nth-child(4) > div > button")[0].click()
    time.sleep(2)
    try:
        index = argv.index('-id')
    except ValueError as e:
        print(e)
    else:
        driver.execute_script(js_cookies_set, "sourceId", argv[index+1])
        
    webDriver(devices)

if __name__ == "__main__":
    run()



