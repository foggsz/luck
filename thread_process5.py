#资源时稀缺的
#计算机资源 竞争计算机的资源
#进程
#至少有1个进程
#进程时竞争计算机资源的基本单位，独立的内存


#单核CPU 永远只能够执行一个应用程序？
#运行速度过快，在不同的应用程序进程之间切换
#vscode、守望先锋、QQ
#进程调度
#算法 挂起 切换到另外一个进程 操作系统原理
#进程/线程 开销是非常大  上下文


#4核


#线程 线程是进程的一部分  一个进程可以有 一个线程或多个线程
#CPU 颗粒度太大了 不能充分利用CPU资源  需要更小的单元 利用CPU
#线程


#进程 分配资源 内存资源
#线程 利用CPU执行代码

#代码 指令 CPU来执行  资源
#访问资源
#线程属于进程  访问进程资源

#更多充分的利用CPU的性能优势
#异步编程
#单核CPU
#4核 A核 B核 并行的执行程序
#python不能充分利用多核CPU优势

#GIL  全局解释器锁 global interpreter lock
#锁  线程安全
#细粒度锁   程序员  主动加锁
#粗粒度锁   解析器  GIL  多核CPU 一个线程执行 一定程度保证进程安全
#a+=1
#bytecode
#python cpython jpython  cpython(GIL)
#多进程  进程通信技术


#python多线程是不是鸡肋
#GIL node.js 单进程 单线程
#线程  非常严重的依赖CPU计算 CPU密集型程序(多线程不适合)  圆周率计算 视频解码
#IO密集型的程序 查询数据库、请求网络资源、读写文件(多线程适合)

#IO密集型  等待

from threading import Thread, local
a = local()
a.b = 1

def worker():
    a.b= 2

t = Thread(target=worker, name='fog')
t.start()
t.join()
print(a.b)    
