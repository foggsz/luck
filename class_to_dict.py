class A:
    a = 10
    def __init__(self, ):
        self.b = 10
        self.c = 11

    @classmethod
    def keys(cls):
        print(111)
        return ("b",)   

    def __getitem__(cls, item):
        return  getattr(cls, item)
#dict ， python序列化对象为字典，可以在keys，筛选要返回的属性，在内置__getitem__，实行对象属性获取
x = dict( A()) 
print(x)  #{'b': 10}

