#应用上下文  AppContext(app)
#请求上下文  RequestContext(Request)
#LocalProxy
#current_app  通过LocalProxy 返回当前App， 指向栈顶
#request      通过LocalProxy 返回当前Request， 指向栈顶
#LocalStatck   
#_app_ctx_stack  
#_request_ctx_stack
#当一个请求发生时，flask 会首先查找_app_ctx_stack里是否存在app对象，如果没有，通过AppContext，自动推入app对象
#之后，通过RequestContext 向_request_ctx_stack推入Request对象。请求结束 两个对象自动从两个栈中退出
#如果不在RequestContext，即视图函数调用AppContext,需要手动推入App上下文。离线应用，单元测试

#with上下文 魔法函数__enter__   __exit__

class  TT:
    def __init__(self,):
        self.a = 10

    def __enter__(self):
        print("进入")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("离开")
        print(exc_type)
        print(exc_val)
        print(exc_tb)
        if exc_type:
            #处理异常
            return True

#exc_type, exc_val, exc_tb 如果不发生异常，则全为None,否则依次为异常类型，异常信息，异常返回栈
#__exit__ 只可以返回True 或False， True,__exit__内部处理了异常，False，外部抛出异常
with TT() as t:
    print(t.a) #10
    1/0    

#webserver
#JAVA、PHP nginx Apache tomcat IIS
#flask 内置服务器  默认单进程、单线程