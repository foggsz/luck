from socketIO_client import SocketIO, LoggingNamespace
import socket
from subprocess import Popen
from store import read, update
import time 
def on_connect(message):
    print('connect')
    
def on_satrt(message):
    print("messssageee")
    print(message)
    socketIO.emit("room", {
        "room": "client1"
    })

def on_disconnect():
    print('disconnect')

def on_clientLimit(data):  #号被限制 停止微信
    limit_name = data.get("limit_name")
    if limit_name:
        temp = {
            "limit_name": limit_name
        }
        update(**temp)
       
def on_clientRefresh(data): #重新刷新微信号
    refresh_name = data.get("refresh_name")
    print(data)
    if refresh_name:
        temp = {
            "refresh_name": refresh_name
        }
        update(**temp)


def  on_clientStart(data):  #启动另一个手机，公众号位置
    statrt_name = data.get("start_name")


socketIO = SocketIO('127.0.0.1', 8000, LoggingNamespace)
# Listen
socketIO.on('start', on_satrt)
socketIO.on('clientRefresh', on_clientRefresh)
socketIO.on('clientLimit', on_clientLimit)
socketIO.on('clientStart', on_clientStart)
socketIO.wait()

# def run_connect():  
#     socketIO = SocketIO('127.0.0.1', 8000, wait_for_connection=True)
#     # Listen
#     socketIO.on('connect', on_connect)
#     socketIO.on('start', on_satrt)
#     socketIO.on('clientRefresh', on_clientRefresh)
#     socketIO.on('clientLimit', on_clientLimit)
#     socketIO.on('clientStart', on_clientStart)
#     socketIO.wait()





