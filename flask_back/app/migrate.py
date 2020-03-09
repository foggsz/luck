from app.models import Users, Societys, Migrates, ExpireLogs
from app.utils  import createPass
from app.citys import citys
import copy
import time
collection = Migrates._get_collection()
def migrate(func, *args, **kws):
    if  type(kws.get("version"))!= int:
        raise ValueError("必须传入版本号")
    version = int(kws.get("version"))
    res  = collection.find({}).sort([("_id", -1)]).limit(1)
    res = list(res)
    res = res[0] if res else {}
    res = dict(res)
    kws.update({"lock": True})
    if not res  or version > res.get("version"):
        collection.insert(kws)
        if args:
            func(*args)
        else:
            func()
    else:
        if not res.get("lock") and version == res.get("version"):
            if args:
                func(*args)
            else:
                func()
            collection.update_one({"_id": res.get("_id")},{"$set": {"lock": True}})
        else:
            return False
        

def init_admin(username="admin"):
    try:
        olddata = Users.objects.get(username=username).to_json()

    except Users.DoesNotExist as e:
        password = createPass(**{
            "password":'123456'           
        })
        Users(roles=['admin'], username=username, password =password).save()

    except Exception as e:
        pass

version = {
    "version":0 ,
    "comment":"初始化管理员用户"
}
def attendCity():
    p = []
    def find_search(arr, keyword, provice=None, city=None):
        nonlocal p
        # if p:
        #     return p
        length = len(arr)
        index = 1
        while index <= length:
            temp = arr[index-1]
            index = index + 1
            if temp.get("name") == keyword:
                p = p + [ [provice, city, temp.get("name")] ]
            else:
                if temp.get("children"):
                    find_search(temp.get("children"), keyword, provice=provice, city=temp.get("name"))
                
        return None

    def find(arr, keyword):
        nonlocal p
        for i , item in  enumerate(arr):
            # if p:
            #     return p       
            if item.get("name") == keyword:
                p.append(item.get("name"))
            else:
                if item.get("children"):
                    res = find_search(item.get("children"), keyword, provice=item.get("name"))
                    # if res:
        
        #     return res
        return p
    citys_xian = copy.deepcopy(citys)
    citys_xians = []
    temp = []
    for i in citys_xian:
        for j in i.get("children"):
                temp = temp +  [k.get("name") for k in j.get("children")]

    collection = Societys._get_collection()
    count = 0
    temp = set(temp)
    # temp = ["朝阳区"]
    for i in temp:
        where = {"org_type":"df"}
        where.update({
            "$or":[
                {"register_organ": {"$regex": i}},
                {"org_listener": {"$regex": i}},
                {"org_name": {"$regex": i}},
                {"org_address": {"$regex": i}},
            ]
        })
        res = collection.find(where, {"_id":1,"org_address":1,"register_organ":1, "org_name":1, "org_address":1, "org_listener":1})
        for k in res:
            p = []
            regions = find(citys, i)
            for index, region in  enumerate(regions):
                update_data = {
                    "region": region
                }
                if k.get("org_address"):
                    update_data["org_address"] = k.get("org_address").replace("联系电话","")
                # if len(regions) == 1:
                #     collection.update_one({"_id": k.get("_id")},{"$set":update_data } )
                #     break
                # else:
                temp = region[1]
                if temp == "市辖区":
                    temp = region[0]
                if  temp in k.get("register_organ", " ") or temp in k.get("org_name", " ")  or temp in k.get("org_listener", " "):
                    collection.update_one({"_id": k.get("_id")},{"$set":update_data } )
                    break
                elif index == len(regions)-1:
                    update_data = {
                        "region": []
                    }
                    collection.update_one({"_id": k.get("_id")},{"$set":update_data } )   
                #     ExpireLogs(**{"info":"编号{0},{1[0]},{1[1]},{1[2]} 无法处理重复地区".format( str(k.get("_id")), region)}   )     

            count = count + 1
            print(count)

    ExpireLogs(**{"info":"社会组织表处理完成，总时长{0}S".format( time.perf_counter()- start ) }).save()
            
migrate(init_admin, **version)

version  = {
    "version" :1,
    "comment" :"增加爬虫接口管理员用户"
}
migrate(init_admin, *("spider_admin",), **version)

version  = {
    "version" :2,
    "comment" :"增加城市 去除联系电话"
}
start = time.perf_counter()
migrate(attendCity, **version)
version  = {
    "version" :3,
    "comment" :"增加脚本管理员用户"
}
migrate(init_admin, *("script_admin",), **version)
# ExpireLogs.objects(info='ssss').update_one(**{'info':'xxx'})
# ExpireLogs.objects(info='yyyy').update(**{'info':'xxx'})