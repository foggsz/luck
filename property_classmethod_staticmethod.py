#python property  classmethod  staticmethod
#property  property 有 getter setter deleter  分别获得，设置，删除一个对象的属性, 并对这些行为做出适当处理，对实例对象使用

class Ob(object):
    _num = 1       #类变量，假如不初始化同名实例变量 ，按照查找规则，实例对象找不到自己的实例变量，会转而去取同名类变量值,但实例变量和类变量并不是同一个内存
    def __init__(self, ):
        # self._num = 100
        self.test = 999
    @property
    def num(self,):  #不定义getter ，此为默认getter
        print("获得值")
        return self._num

    @num.setter
    def num(self, value):
        print("赋值")
        self._num = self._num + value

    @num.deleter
    def num(self,):
        print("进行删除操作")
        del self._num

    @staticmethod
    def addNum(value):
        Ob._num= Ob._num + value

    @classmethod
    def get_cls(cls, ):  
        cls = cls()
        cls._num = 100 #这样类似于工厂函数，产生新对象出去
        return cls

#staticmethod 定义一个静态类方法 ,静态类方法无法访问实例变量，只可以访问类变量,类方法，实例和类对象共享.可以当作是一个普通函数
#classmethod 定义一个类方法，第一个参数指的是对象本身，也就是这个方法既可以访问实例属性，也可以放静态属性,可以作为工厂函数
# ，或者需要实例和类交互使用
x = Ob()
x.num = 10
print(x.num)  #此时赋值，值为11
print(Ob._num)  #类变量为1, 1
x.addNum(11)
print(x.num)   #仍是11
print(Ob._num)  #12
new_x = x.get_cls()
print(new_x.num)  #100
print(Ob._num)    #12
Ob._num = 999
print(4544545)


#可调用对象, 实例对象方法调用, 简化方法调用过程 ,统一接口  __call__
class A:
    def __init__(self, num, numtwo):
        self.num = num
        self.numtwo = numtwo
    def __call__(self, num):
        print(num)
        

a = A(1,2)
a(3)


