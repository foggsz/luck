from multiprocessing import Process, Pool, Pipe,Value, Array, Lock, Manager , managers, Queue
from threading import Thread, local, current_thread
import os
import queue
import random 

g_data = local()
def job(x):
    return 123
def job2(x,y):
    return 123456

def job3(conn):
    conn.send("sssdsdsd")
    conn.close()

def job4(x):
    g_data.name = x
    text()

def text():
    print(g_data.name, current_thread().name)

def job5(x, arr, i=1):
    print(x.value)
    for i in range(len(arr)):
        arr[i] = arr[i]**2
        
    for  i in range(10):
          x.value =  x.value  + i
          print(x.value, os.getpid())
          
def job6(x, arr):
    for i in range(10):
        x.value = x.value  + 3
        print(x.value, os.getpid())


class  JobClass(object):
    def add(self, x, y):
        return x+y
    def decrease(self, x, y):
        return x - y    
class JobManger(managers.BaseManager):
    pass

JobManger.register('jobclass', JobClass)    
class QManger(managers.BaseManager):
    pass

class Worker(Process):
    def __init__(self, q):
        super().__init__()
        self.q = q

    def run(self):
        self.q.put('local  hello')

task_queue = queue.Queue()
result_queue = queue.Queue()

def return_task_queue():
    global task_queue
    return task_queue

def return_result_queue():
    global result_queue
    return result_queue   

if __name__ == "__main__":
    parent_conn, child_conn = Pipe() 
    lock = Lock()
    p = Pool()
    res = p.map(job, [7,8,9])
    print(res)
    p = Process(target=job3, args=(child_conn,))
    p.start()
    print(parent_conn.recv())
    p.join()
    print(9999)
    t1 = Thread(target=job4, args=("234234", ), name="t1")
    t2 = Thread(target=job4, args=("99999", ), name="t2")
    t1.start()
    t1.join()
    t2.start()
    t2.join()
    num = Value('i', 10, lock=lock)
    num_arr = Array('i', range(10))
    p = Process(target=job5, args=(num,num_arr,))
    p.start()
    p1 = Process(target=job6, args=(num,num_arr))
    p1.start()
    p.join()
    p1.join()
    print(num.value)
    # print(list(num_arr))
    with JobManger() as jobManger:
        jobclass = jobManger.jobclass()
        print(jobclass.add(4, 3))         # prints 7

    w = Worker(Queue())   #只能使用进程的Queue
    w.start()
        
    QManger.register('task_queue', callable=return_task_queue)
    QManger.register('result_queue', callable=return_result_queue)
    m  = QManger(address=("127.0.0.1", 500), authkey=b'abc')
    m.start()
    task = m.task_queue()
    result = m.result_queue()
    # 放几个任务进去:
    for i in range(10):
        n = random.randint(0, 10000)
        print('Put task %d...' % n)
        task.put(n)
    # 从result队列读取结果:
    print('Try get results...')
    for i in range(10):
        r = result.get(timeout=10)
        print('Result: %s' % r)
    # while not result.empty():
    #     r = result.get(timeout=10)
    #     print('Result: %s' % r)
    # 关闭:
    while True:
        try:
            r = result.get(timeout=10)
            print('Result: %s' % r)
        except Exception as e:
            print(e)  
            m.shutdown()
            break

    print('master exit.')
   
