#greenlet switch来进行协程切换,属于人工切换
import greenlet
import threading as th
import time
def f1():
    print("f1")
    g2.switch()
    print("f1之后")

def f2():
    print("f2")
    g1.switch()
    print("f2之后")

g1 = greenlet.greenlet(f1)
g2 = greenlet.greenlet(f2)
g1.switch()
print(g2.dead)
#f1
#f2
#f1之后
#False
#但是没有打印F2之后，因为左后调用f1之后，没有调回f2, 可能会造成内存泄漏

#python Event  进程、线程间通讯
#Event.set() 设置标志位
#Event.clear() 清除标志位
#Event.wait()  等待设置标志位,可以设置等待秒数

event = th.Event()
def green():

    if event.is_set():
        print("现在开始通讯")
    else:
        print("等待通讯连接")
        event.wait()
        print("已经链接")
def t2():
    time.sleep(5)
    event.set()

t1 = th.Thread(target=t1,)
t2 = th.Thread(target=t2,)
t1.start()
t2.start()