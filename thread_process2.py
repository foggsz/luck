
from multiprocessing.managers import BaseManager
class QManger(BaseManager): 
    pass

QManger.register('task_queue')
QManger.register('result_queue')
m  = QManger(address =("127.0.0.1",500), authkey=b'abc' )
m.connect()
task_queue = m.task_queue()
result_queue = m.result_queue()
while not task_queue.empty():
    print("接受到：", task_queue.get())

for i in range(10):
   result_queue.put(i) 

