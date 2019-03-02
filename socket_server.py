import socket
import threading
import socketserver
#创建一个socket 的客户端
#socket 传输的都是字节对象
server_address = ("127.0.0.1", 9999) #socket服务器地址这里是一个元组
# socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #指定ip协议， 传输层协议（UDP/TCP）,这里是tcp
# socket_server.bind(server_address)
# socket_server.listen(10)
import time

def handle_socket(socket, addr):
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        print("data")
        print(data)
        if data.decode("utf-8") == "exit" or not data:
            sock.send(b"byebye")
            break
    sock.close()
   
# while True: #需要线程来处理多个连接请求
#     sock, addr = socket_server.accept() #返回当前连接的sockt连接
#     t = threading.Thread(target=handle_socket, args=(socket, addr,))
#     t.start()
class ThreadingTCPServerHanler(socketserver.BaseRequestHandler):
        def handle(self):
            self.request.send("霓虹".encode("utf-8"))
            self.request.send("霓虹1".encode("utf-8"))
            cur_thread = threading.current_thread()
            print( "当前线程{}".format(cur_thread.getName() ) )
            data = str(self.request.recv(1024), 'utf-8')
            print(data)
            print("----------")
            data = str(self.request.recv(1024), 'utf-8')
            print(data)
            self.request.send("来自服务器的再见0".encode("utf-8"))
            # self.request.close()
            self.request.send("来自服务器的再见".encode("utf-8"))
            # self.finish()
            # self.request.close()
#socketserver  socket高级接口
with socketserver.ThreadingTCPServer(server_address, ThreadingTCPServerHanler)  as server:#指定地址， 处理类需继承重写hanler
    server.serve_forever()
