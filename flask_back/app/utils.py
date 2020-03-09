from werkzeug.security import generate_password_hash, check_password_hash  #自带加密算法
from  app.models  import Users
import redis
from bson import  ObjectId
from app.citys import  citys
def createPass(**kws):
    encryptStr = generate_password_hash(kws.get("password")) 
    hash_password = encryptStr 
    encryptStr =  encryptStr.split("$")
    method = encryptStr[0]
    salt = encryptStr[1]
    return {
        "hash_password": hash_password,
        "salt": salt,
        "method": method
    }

def verifyPass(**kws):
    username = kws.get("username")
    password = kws.get("password")
    data = Users.objects.only('password').get( __raw__={'username': username } )
    if data and data["password"]:
        res = check_password_hash(data["password"]["hash_password"], password)
        if res:        
            return res , None , str(data["_id"])
        else:
            return res ,  "密码错误" , None
    else:
        return False, "账号错误"  , None 
    
def verifyRoles(userId, rolename):
    if type(userId) == str:
        userId = ObjectId(userId)
    try:       
        res = Users.objects.only("roles").get(__raw__={'_id':userId, 'roles':rolename}).to_json() 
    except Users.DoesNotExist as e:
        res = False
    return res

class ClientSet(object):
    clients = set()

    def __init__(self, ):
        pass
    
    def add(self, key):
        self.clients.add(key)

    def remove(self, key):
        try:
            self.clients.remove(key)
        except KeyError as e:
            print("删除失败,不存在的键名")

    def clear(self, key):
        self.clients.clear()

    def pop(self, key):
        try:
            self.clients.pop()
        except Exception as  e:
            print("随机删除失败,集合为空")

    def isexits(self, key):
        for i in self.clients:
            if i == key:
                return key
        return  False
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            temp = self.clients.pop()
        except Exception as e:
            raise StopIteration()
        else:
            return temp

def search_city(keyword):
    temp = []
    index  = []
    def search(keyword):
        nonlocal index
        for i, item in  enumerate(citys):
            if item.get("name")  == keyword:
                index = index + [i]
                return item
            else:
                for i1, item_child in  enumerate(item.get("children")):
                    if item_child.get("name")  == keyword:
                        index = index + [i, i1]
                        return item
                    else:
                        for i2, item_child1 in enumerate(item_child.get("children")):
                            if item_child1.get("name")  == keyword:
                                index = index + [i, i1, i2]
                                return item
        return None
    res = search(keyword)
    if res:     
        temp = [] 
        temp.append(res.get("name"))
        child = res.get("children")
        if len(index) == 1:
            for item in  child:
                # temp = temp + [item.get("name")]
                temp = temp + [item.get("name") for  item in item.get("children") if item.get("name")]
        elif len(index) == 2:
            child = child[index[1]]
            # temp = temp + [ child.get("name") ]
            child = child.get("children")
            temp = temp + [item.get("name") for  item in child if item.get("name")]
        
        elif len(index) == 3:
            child = child[index[1]]
            temp = temp + [ child.get("name")]
            child = child.get("children")[index[2]]
            temp = temp + [ child.get("name")]
        return temp
    return None  

def  cal_weights():
    arr = [          #左到右， 上至下依次为  社会组织名称  法定代表人姓名  行政区划  业务范围 成立登记日期
        [1, 1, 7, 5, 7],
        [1, 1, 7, 5,  7],
        [1/7, 1/7, 1, 1/3,1],
        [1/5, 1/5, 3, 1, 3],
        [1/7, 1/7, 1, 1/3,1],
    ]

    # arr =  [
    #     [1,9,7,5],
    #     [1/9,1,1/3,1/5],
    #     [1/7,3,1,1/3],
    #     [1/5,5,3,1]

    # ]
    arr_keys = ["org_name", "law_men", "region", "work_range", "timerange"]
    constat_tables = {
        4: 0.90,
        5: 1.12,
        6: 1.24,
        7: 1.32,
    }
    import numpy as np
    #转换成矩阵
    matrix = np.array(arr)

    #求和
    sum_row = matrix.sum(axis=0)
    sum_row = np.array([sum_row])
    matrix =  np.concatenate( (matrix, sum_row) )
    rows , cols  = matrix.shape
    #原矩阵 每一列元素除以列的和获得新矩阵
    new_matrix = []
    for col in matrix.T:
        new_col = []
        for index, val in enumerate(col):
            if index == rows-1:
                break
            else:
                temp = val / col[rows-1]
                new_col = new_col + [temp]
        
        new_matrix.append(new_col)
    new_matrix = np.array(new_matrix).transpose()
    # print(feature_sum_col)
    #添加 每列总数， 再计算出每行总数，添加到新矩阵
    feature_sum_col = new_matrix.sum(axis=0)
    feature_sum_col = np.array([feature_sum_col])
    new_matrix = np.concatenate((new_matrix, feature_sum_col), axis=0)
    feature_sum_row = new_matrix.sum(axis=1)
    feature_sum_row = np.array([feature_sum_row])
    new_matrix = np.concatenate((new_matrix, feature_sum_row.T), axis=1)

    #计算权重, 填入新举证
    temp  =  new_matrix[:,-1]
    feature_total = new_matrix[-1,-1]
    rates = np.divide(temp, feature_total)
    rates = np.array([rates])
    new_matrix = np.concatenate((new_matrix, rates.T), axis=1)

    #计算 最大特征根 ,原矩阵X新矩阵的比率航/新矩阵的比率航
    # max_feature = 
    rates = rates[0,0:-1]
    feature_row = matrix[0:-1].dot(rates)    #原矩阵剔除最后一行总和  得到每行特征值

    feature_row = np.divide(feature_row, rates   )
    feature_row_total = [feature_row.sum()]
    feature_row =  np.concatenate((feature_row, feature_row_total), axis=0)

    #合并特征值到新矩阵
    feature_row_matrix = np.array([feature_row])
    new_matrix =  np.concatenate((new_matrix, feature_row_matrix.T), axis=1)
    arerge_feayure = feature_row_total[0] / len(arr)

    #是否一致 ，查看相关系数表
    res = {"weights": {} }
    constant_index  =  (arerge_feayure - len(arr))/ (len(arr)-1)
    if constant_index / constat_tables.get(len(arr)) <0.1:
        res.update({
            "info": "相关系数，一致性指标为{0}，低于正常界限0.1，属于合理范围".format(constant_index )
        })
    else:
        res.update({
            "info": "相关系数，一致性指标为{0}，高于正常界限0.1，相关系数不合理，请重试".format(constant_index )
        })

    for i, rate in enumerate(rates):
        res["weights"].update({
            arr_keys[i]: rate
        })

    return res
    
# cal_weights()