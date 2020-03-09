from subprocess import Popen, PIPE
import os
import shlex
from  point import get_point, points
import time
from store import read, update
def start():
    adb_start = ['adb', 'shell']

    """
    按钮名字
    search_btn     
    telList_btn
    gzhDetail_btn
    """
    step0 = b"""
    am start -n  com.tencent.mm/.ui.LauncherUI 
    exit
    """    
    pipe = Popen(adb_start, stdin=PIPE, stdout=PIPE)
    outs, errs = pipe.communicate(input=step0, timeout=15)
    telList_x, telList_y = get_point("telList_btn")   #通讯录坐标
    step1 = "adb shell input tap  {0}  {1}".format(telList_x,  telList_y)
    pipe = Popen(step1, shell=True)
    pipe.wait()


    gzh_x, gzh_y = get_point("gzh_btn")   #公众号按钮
    step2 = "adb shell input tap  {0}  {1}".format(gzh_x,  gzh_y)
    pipe = Popen(step2, shell=True)
    pipe.wait()


def get_points(findName=None):
    total, gzh_total= get_point("swipe0", findName)   #滑动开始，获得公众号底部总数 
    print(points)

def main_steps(position, key):
    step4 = "adb shell input tap {0} {1} ".format(position[0], position[1])
    pipe = Popen(step4, shell=True)
    pipe.wait()


    gzhDetail_x , gzhDetail_y = get_point("gzhDetail_btn")   #公众号详情按钮
    step5 ="adb shell input tap {0}  {1}".format(gzhDetail_x, gzhDetail_y)    
    pipe = Popen(step5, shell=True)
    pipe.wait()
    # swipe1_x, swipe1_y = get_point("swipe1")   #公众号详情按钮滚动起点
    # step6 = """
    #     adb shell input swipe1  {0}  {1}  0  0
    # """.format(swipe1_x,  swipe1_y)
    # pipe = Popen(step6, shell=True)
    # pipe.wait()


    allMessage_x , allMessage_y = get_point("allMessage_btn")   #全部消息按钮
    step7 = "adb shell input tap  {0}  {1} ".format(allMessage_x,  allMessage_y)
    pipe = Popen(step7, shell=True)
    pipe.wait()

    #打开页面休息5秒
    time.sleep(5)
    
    #返回列表页面操作
    step8 = """
        input keyevent 4
        input keyevent 4
        input keyevent 4
        exit
    """
    step8 = bytes(step8,encoding="utf-8")
    pipe = Popen(adb_start,stdin=PIPE, stdout=PIPE)
    pipe.communicate(input=step8)
    
    # #是否需要刷新的页面
    # refresh(key)
    # #是否被限制，停止
    # stop()

    
def if_exisit(key):
    keys = [ v for v  in   i  for i  in [ list(i.keys()) for i in points["map"] ] ]
    keys = set(keys)
    if key in keys:
        return True
    else:
        return False

#是否被限制直接停止  杀掉微信
def stop():
    temp = read()
    limit_name = temp.get("limit_name")
    update(**{"limit_name": None})
    if limit_name:
        pipe = Popen("adb shell am force-stop com.tencent.mm", shell=True)
        pipe.wait()

#重新刷新失效公众号操作
def refresh(current_name):
    temp = read()
    refresh_name = temp.get("refresh_name")
    update(**{"refresh_name": None})
    if refresh_name:
        if if_exisit(refresh_name):
            find_fresh(refresh_name,  current_name)   #失效的公众号名字   当前点击的公众号名字


def find_fresh(refresh_name, current_name, refresh_name_index  = None, current_name_index  = None):
    
    if  refresh_name_index and current_name_index:
        if refresh_name_index == current_name_index:                 #处在同一数组 即同一屏幕 不需要滑动 再次点击下失效坐标
            temp_pos = points["map"][refresh_name_index].get(temp_pos)
            pipe = Popen("adb shell input tap   {0[0]}  {0[1]}   ".format(postion), shell=True)
            pipe.wait()
            return 
        elif  refresh_name_index < current_name_index:   #不处在同一数组 需要滚屏两者下标差值，再点击
            temp_total = int(current_name_index-refresh_name_index)
            for i in range(temp_total):
                temp_current_index = int(current_name_index - i)
                temp_pos = points["map"][temp_current_index].get("swipe")                      
                pipe = Popen("adb shell input tap   {0[0]}  {0[1]}   ".format(temp_pos), shell=True)
                pipe.wait()          
            return 
        else:
            print("不存在的情况，注意注注意")
            return 

    for index, item in enumerate(points["map"]):
        temp_keys = item.keys()
        if refresh_name in temp_keys:
            refresh_name_index = index
        if current_name in temp_keys:
            current_name_index = index

    return find_fresh(refresh_name, current_name, refresh_name_index  = refresh_name_index, current_name_index  = current_name_index)


#points = {'map': [{'爱洁洗车': ['140', '233'], '八戒投': ['140', '406'], '宝元e代客': ['140', '535'], '北京云途明志科技有限公司': ['140', '664'], '碧桂园生活': ['140', '793'], 'CityOn熙地港郑州购物中心服务号': ['140', '966'], '大班幻美空间': ['140', '1139'], '大勤云商': ['140', '1268'], 'swipe': [140, 1268, 720, 190]}, {'大众约车': ['140', '206'], '德派茶事': ['140', '335'], '电影演出票': ['140', '464'], '多点优惠': ['140', '593'], 'ELLE美颜社': ['140', '767'], '二更': ['140', '896'], '分众专享': ['140', '1069'], 'FMT8可乐姐姐': ['140', '1198'], 'swipe': [140, 1268, 720, 190]}, {'weibo_tencent': ['140', '179'], 'yinglianapp': ['140', '308'], 'gh_598bff80731d': ['140', '437'], 'gh_54fb76b42e01': ['140', '566'], '该帐号已注销': ['140', '695'], '公众平台测试账号系统': ['140', '824'], '关爱八卦成长协会': ['140', '953'], '海珀兰轩': ['140', '1127'], '河南电信': ['140', '1256'], 'swipe': [140, 1268, 720, 190]}, {'河南同步货运': ['140', '186'], '汇泰汽配': ['140', '315'], '佳顺租赁': ['140', '488'], '借贷宝': ['140', '617'], '金宝人力河南鑫保': ['140', '746'], '可口可乐': ['140', '920'], 'LEGO乐高': ['140', '1094'], '流量宝': ['140', '1223'], 'swipe': [140, 1268, 720, 190]}, {'罗辑思维': ['140', '156'], '麦客MikeCRM': ['140', '330'], '梦乐城': ['140', '459'], '米家有品': ['140', '588'], 'MoPaaS': ['140', '717'], '南孚店主服务平台': ['140', '891'], '牛牛理财': ['140', '1020'], '票时代': ['140', '1194'], 'swipe': [140, 1268, 720, 190]}, {'睿介寻人': ['140', '185'], '睿介寻子': ['140', '314'], '商都房产': ['140', '488'], '斯柯达车友会': ['140', '617'], '松山湖物业': ['140', '746'], '汤面小生': ['140', '920'], '天冰冰淇淋': ['140', '1049'], '天湖网络': ['140', '1178'], 'swipe': [140, 1268, 720, 190]}, {'tony的接口测试号': ['140', '146'], '完美地产营销': ['140', '284'], '微信公众平台': ['140', '413'], '微信公众平台测试号': ['140', '542'], '微信卡包': ['140', '671'], '微信游戏': ['140', '800'], '微信支付': ['140', '929'], '微信支付商户助手': ['140', '1058'], 'WLDloan': ['140', '1187'], 'swipe': [140, 1268, 720, 190]}, {'wxid_l6zvws6oeg9421的接口测试号': ['140', '146'], '小罐茶': ['140', '298'], '小树有机': ['140', '427'], '洗车净': ['140', '556'], '新田360广场': ['140', '685'], '新田360广场郑州国贸店': ['140', '814'], '寻网': ['140', '943'], '烟台吃喝玩乐': ['140', '1117'], '亚新美好艺境': ['140', '1246'], 'swipe': [140, 1268, 720, 190]}, {'益美传媒': ['140', '174'], '优乐美奶茶': ['140', '303'], '涨芝士啦': ['140', '477'], '中国电信': ['140', '606'], '中国电信营业厅': ['140', '735'], '中联天城': ['140', '864'], '众银家': ['140', '993'], '众银客': ['140', '1122'], '诸葛理财': ['140', '1251'], 'swipe': [140, 1268, 720, 190]}], 'telList_btn': ['234', '1237'], 'gzh_btn': ['124', '488'], 'swipe0': (10, 76)}
def main_run():
    for item in points["map"]:
        swipe  = None
        for key, val in item.items():
            # if store.get("start_name"):  #如果有起始位置
            # else:
            if key == "swipe":
                swipe =  val
            else:
                main_steps(val, key)

        if swipe:
            step_swider = "adb shell input swipe {0[0]}  {0[1]}   {0[2]}  {0[3]}  2000".format(swipe)
            pipe = Popen(step_swider, shell=True)
            pipe.wait()

if __name__ == "__main__":
    start()
    get_points()
    #退出重新进,再次进入公众号
    step3 = "adb shell input keyevent 4"
    pipe = Popen(step3, shell=True)
    pipe.wait()

    gzh_x, gzh_y = get_point("gzh_btn")   #公众号按钮
    step2 = "adb shell input tap  {0}  {1}".format(gzh_x,  gzh_y)
    pipe = Popen(step2, shell=True)
    pipe.wait()
    main_run()