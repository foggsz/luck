#python中的协程，使用Generator
#第一种方法 列表表达式中括号便小括号
x = ( i for i in range(10) )
print(type(x))  #<class 'generator'>
print(next(x))  #0

#第二 yield关键词，该函数即变成genertor
def yieldFuc():
    for i in range(10):
        yield i
        print(i)
yield_fuc = yieldFuc()
print(yield_fuc.__next__()) #0
print(yield_fuc.__next__()) #第二次调用函数会在yield第二行执行,先打印0，再打印1
print(next(yield_fuc)) #第三次同上，先打印1，再打印2

#__next__  next 功能都是取generator的值，generator 是可遍历的,可以转化为list
for i in yield_fuc:  #这里为3-9
    print(i)
print(list(yield_fuc))  #这里为空，因为上面应该把generator 取完了，用列表取值不会报错
# 但是如果再print(next(yield_fuc)) 报错 =>StopIteration

#以上说明generator 类似普通队列， 返回值的取出是先进先出，可以利用这个特性做消费和生产者模式
#genertor有send属性，send属性类似于next和__next__()，但是有所不同，send可以发送参数给generator，供generator使用,但是第一次调用generator 不能发送有值的对象，只能发送None,
#据了解，源码就是这样规定的。过程类似，send 调用generator， 首先获得yield的返回值，然后send将某些参数传给yield 处,不是第二行！yield 把它交给某个变量，供yield下面代码使用，

def consumer():
    result = ''   #返回给生产者的结果
    while True:
        job  = yield result
        if job  is None:
            return  #yield return不用写返回值

        print("收到生产者任务{0}".format(job))
        result = "消费者完成任务{0}".format(job)
        

def producer(c):
    c.send(None)
    for i in range(5):
        res = c.send(i)  
        print(res)

c = consumer()  #这时的generator 无限大，不能转化列表会死机
producer(c)

#python有两个常用外部协程第三方库，可以提高效率，处理并发，greentlet和gevent。greentlet需手动切换线程，gevent可以自动切换线程但需要打monkey补丁


