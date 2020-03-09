import pyautogui
import time
import re
import datetime
import random
import time
pyautogui.FAILSAFE = True
down_scroll = -7.3 #滚动距离
argv_height  = 51  #公众号选中后高度
step = argv_height #每次向下移动
page_height =  523 #页面底部距X轴的高度
line_height = 33   #每组距下一条线高度
startX = 180   #起始位置X
startY = 156   #起始位置Y
import time
import pytesseract
from PIL  import Image, ImageGrab, ImageEnhance, ImageFilter
start = time.perf_counter()

total  = pyautogui.prompt("输入公众号总数")
total = eval(total)
# print(total)
# #起点位置
# p = {
#     "x": 30,
#     "y": 200
# }
# pyautogui.click(**p)

#公众号位置
# pos = pyautogui.locateOnScreen("./gzh_btn.png")
# if pos is None:
#     pyautogui.alert('无法识别公众号按钮')
#     exit()
# p = {
#     "x": pos[0],
#     "y": pos[1],
#     "pause": 1
# }
# pyautogui.click(**p, clicks=2)
pyautogui.click(x=40, y=250, clicks=2)

# 识别公众号总数  和折叠按钮在一张截图
img =  Image.open("./collapse.png")
# img_two = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
# # img_two = ImageEnhance.Contrast(img).enhance(5)
# img_two = img_two.convert("L")
# img_two.show()
# res = pytesseract.image_to_string(img_two, lang="chi_sim")
# print(res)
error = None
# if res is None:
#     error = True
# total = re.search('[0-9]+',res)
# if total is None:
#     error = True
# total = int( total.group())
# print(total)
# exit()

#公众号折叠按钮  
# pos = pyautogui.locateOnScreen(img)
# if pos is None:
#     pyautogui.alert('无法识别公众号折叠按钮')
#     exit()

p = {
    "x": 149,
    "y": 105,
    "pause": 1
}
# pyautogui.moveTo(x=p["x"]-8, y=p["y"])
pyautogui.click(**p,clicks=1)
# 592 389 
# 692 405
look_btn_img = ImageGrab.grab(bbox=(592,389,692,405))
# pyautogui.moveRel(None, 100)
# pyautogui.click()
#查看消息按钮  
# pos = pyautogui.locateOnScreen("./look_btn.png")
# if pos is None:
#     pyautogui.alert('无法识别查看消息按钮')
#     exit()

def run():
    global p
    pos = pyautogui.locateOnScreen(look_btn_img)
    btn_x, btn_y, btn_w, btn_h= pos
    # pos = pyautogui.locateOnScreen("./look_btn.png")
    # btn_x, btn_y, btn_w, btn_h= pos
    for i in range(total):
        # pos = pyautogui.locateOnScreen(look_btn_img)
        # btn_x, btn_y, btn_w, btn_h= pos
        pyautogui.press("down", interval=1)
        p = {
            "x": btn_x,
            "y": btn_y,
        }
        pyautogui.click(**p)
        time.sleep(5)
        # time.sleep(random.randint(10,20))
        # x = random.randint(1,3)
        pyautogui.scroll(-1)
        #关闭历史消息
        # p = {
        #     "x": 256,
        #     "y": 119,
        #     "pause": 3
        # }
        # pyautogui.press()
        pyautogui.hotkey('command', 'w', pause=1)
        time.sleep(1)
        
if error  is None:
    run()
    end = time.perf_counter()- start
    end = int(end)
    end = datetime.timedelta(seconds=end)
    pyautogui.alert('共点击了{0}次, 花费了{1}'.format(total, end))
   

