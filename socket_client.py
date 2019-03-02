import socket
#创建一个socket 的客户端
#socket 传输的都是字节对象
socket_cilent = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #指定ip协议， 传输层协议（UDP/TCP）,这里是tcp
server_address = ("127.0.0.1", 9999) #socket服务器地址这里是一个元组
socket_cilent.connect(server_address)
receive = socket_cilent.recv(1024,)  #指定接收字节数量,默认接收时阻塞模式
print(receive.decode('utf-8'))
receive = socket_cilent.recv(1024,)  #指定接收字节数量,默认接收时阻塞模式
print(receive.decode('utf-8'))
socket_cilent.send(b'exit1')
socket_cilent.send(b'exit2')
socket_cilent.send(b'exit3')
receive = socket_cilent.recv(1024,)  #指定接收字节数量,默认接收时阻塞模式
print(receive.decode('utf-8'))
receive = socket_cilent.recv(1024,)  #指定接收字节数量,默认接收时阻塞模式
print(receive.decode('utf-8'))
socket_cilent.send(b'exit4')
# while True:
#     socket_cilent.sendall(b'exit')
# socket_cilent.close()
#只要没有达到接收字数限制，连续多次调用sendall发送消息，服务器端一次性可以全部收到
#sock必须 一方执行发送动作， 一方执行接收动作
