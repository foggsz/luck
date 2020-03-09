# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, abort, request
from app.models import Source, Dossiers, Societys
from bson.json_util import  dumps, ObjectId, loads 
# from bson.json_util import loads as bason_loads
from json import loads
from app.auth import verify_token
from datetime import datetime
from pymongo import DESCENDING, ASCENDING
import time
import re
import jieba
from app.utils import cal_weights
from functools import reduce

class Dossier(Resource):
    def __init__(self, ):
        self.parser = reqparse.RequestParser()

    decorators = [verify_token]

    def get(self, returnToken=None, userId=None):
        self.parser.add_argument('org_name', type=str, help="请传入字符串类型", default="")
        self.parser.add_argument('unite_credict_code', type=str, help="请传入字符串类型")
        self.parser.add_argument('law_men', type=str, help="请传入字符串类型")
        self.parser.add_argument('region', type=str,  action="append", default=[])
        self.parser.add_argument('timerange', type=int,  action="append", default=[], help="请传入整数数组")
        self.parser.add_argument('org_classify', type=str)
        self.parser.add_argument('sort', type=str)
        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('limit', type=int, default=10)
        self.parser.add_argument("dosser_id", type=str)
        params = self.parser.parse_args()
        dosser_id = params.get("dosser_id")
        if dosser_id:
            res = Dossiers.objects.get(_id=ObjectId(dosser_id)).to_json()
            for item in res.get("society_ids", []):
                temp = item.pop("_id")
                if temp.get("$oid"):
                    item["_id"] = temp.get("$oid")

            for item in res.get("source_ids", []):   
                temp = item.pop("_id")
                if temp.get("$oid"):
                    item["_id"] = temp.get("$oid")

            return {
                "data": res,
                "code": 200,
                "returnToken": returnToken
            }
        page = params.pop("page")
        limit = params.pop("limit")
        where =  {}
        for key, val in params.items():
            if key == 'region':
                if val:
                    where.update({"region": {"$all": val} })
            else:
                if val:
                    if key == "timerange": 
                        where.update({"org_create_date": {"$gte": val[0], "$lte": val[1]} })
                    where.update({
                        key: {"$regex": val}
                    })

        Dossiers_collection = Dossiers._get_collection()
        total = Dossiers_collection.find(where).count()
        res = Dossiers_collection.aggregate([
            {"$match": where},
            {
                "$unwind": { "path" : "$society_ids", "preserveNullAndEmptyArrays":True}
            },
            {
                "$unwind": { "path" : "$source_ids", "preserveNullAndEmptyArrays":True}
            },
            {
                "$lookup": {
                    "from": 'society',
                    "localField": 'society_ids._id' ,
                    "foreignField": '_id',
                    "as": "society_data"
                }
            },
            {
                "$lookup": {
                    "from": 'source',
                    "localField": 'source_ids._id' ,
                    "foreignField": '_id',
                    "as": "source_data"
                }
            },
            {
                "$group": {"_id":"$_id", "data": {"$mergeObjects": "$$ROOT"} }
            },
            {
                "$project": {
                    "_id": 0,
                }
            },
            {
                "$sort": {
                    "data.society_ids.f_score": -1,
                    "data.source_ids.f_score": -1,
                    "data.org_create_date": -1,
                    "data.createAt": -1,
                    "data.updateAt": -1,
                },
            },
            {
                "$skip": (page-1)*limit
            },
            {
                "$limit": limit
            },
        ])
        res = loads(dumps(res))
        resData = {
            "data": res,
            "total": total
        }
        return {
            "items": resData,
            "code": 200,
            "returnToken": returnToken
        }

    def post(self, returnToken=None, userId=None):
        params = self.parser.parse_args()
        self.parser.add_argument('org_name', type=str, help="请传入字符串类型", default="")
        self.parser.add_argument('unite_credict_code', type=str, help="请传入字符串类型")
        self.parser.add_argument('law_men', type=str, help="请传入字符串类型")
        self.parser.add_argument('work_range', type=str, help="请传入字符串类型")
        self.parser.add_argument('region', type=str,  action="append", default=[])
        # self.parser.add_argument('timerange', type=int, help="请传入整数类型", action="append", default=[])
        self.parser.add_argument('org_create_date', type=int)
        self.parser.add_argument('org_classify', type=str, help="请传入字符串类型",)
        self.parser.add_argument('logo_url', type=str, help="请传入字符串类型",)
        self.parser.add_argument('extra', type=str, help="请传入字符串类型",)
        self.parser.add_argument("society_ids", type=dict, action="append", default=[])
        self.parser.add_argument("source_ids", type=dict, action="append", default=[])
        self.parser.add_argument("dosser_id", type=str)
        params = self.parser.parse_args()
        source_ids = params.get("source_ids")
        society_ids = params.get("society_ids")
        try:
            for item in source_ids:
                item['_id'] = ObjectId(item.get('_id'))
            for item in society_ids:
                item['_id'] = ObjectId(item.get('_id'))
            dosser_id = params.pop("dosser_id", None)
            if dosser_id:
                params.update({
                    "updateAt": datetime.utcnow()
                })
                res = Dossiers.objects(_id= ObjectId(dosser_id) ).update_one(**params)
                return {
                    "code": 200,
                    "returnToken": returnToken
                }
        except Exception as e:
            abort(400, **{"message":{"must":"不合法的参数"}})
            
        data = Dossiers(**params)
        data.save()
        res_id = str( data['auto_id_0'] )
        
        return {
            "res_id": res_id,
            "code": 200,
            "returnToken": returnToken
        }

class DossierMatch(Resource):
    def __init__(self, ):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('org_name', type=str, help="请传入字符串类型", default="")
        self.parser.add_argument('unite_credict_code', type=str, help="请传入字符串类型")
        self.parser.add_argument('law_men', type=str, help="请传入字符串类型")
        self.parser.add_argument('work_range', type=str, help="请传入字符串类型")
        self.parser.add_argument('region', type=str,  action="append", default=[])
        self.parser.add_argument('timerange', type=int, help="请传入整数类型", action="append", default=[])
        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('limit', type=int, default=10)
        
    decorators = [verify_token]
    def generateWeights(self, weights, filter_keys=['org_name',  'law_men', 'work_range', 'region', 'timerange'] ):
        params = self.parser.parse_args()
        front_keys = [ key for key, val in params.items()  if  val and key in filter_keys ]  #前台展示比例
        weights_front = weights.copy()
        weights_front = list( weights_front.items() )
        def add(x, y):
            if type(x)  == tuple:
                if x[0] in front_keys:
                    x  = x[1]
                else:
                    x  = 0

            if type(y) == tuple:
                if y[0] in front_keys:
                    y  = y[1]
                else:
                    y = 0     
            
            return x+ y

        total_rate = reduce(add,  weights_front)
        def filter_front(item):
            key, val = item
            if  key in front_keys:
                if val  >= 1:
                    return item
                item = ( key, val * (1/total_rate) )
                return item
            else:
                return (key, 0)
                
        weights_front  = dict( map(filter_front, weights_front ) )
        return weights_front

    def get(self, returnToken=None, userId=None):    #匹配社会组织
        params = self.parser.parse_args()
        where = {}
        weights_obj  = cal_weights()
        weights = weights_obj.get("weights")
        weights_front  = self.generateWeights(weights)
        org_name_len = 0
        for  key, val in params.items():
            if not val:
                continue
            if key == 'region' :
                where.update({"region": {"$all": val} })
            elif key == 'timerange':
                if val:
                    if len(val) == 2:
                        where.update({"org_create_date": {"$gte":val[0], "$lte":val[1]} })
                    elif len(val) == 1:
                        where.update({"org_create_date": {"$gte":val[0]} })
                else:
                    continue
            else:
                if key == "unite_credict_code":
                    continue
                if key!= "page" and key!="limit": 
                    val = val.strip()
                    if val:
                        if key == "org_name":
                            org_name_len = len(val.replace(" ",""))
                            temp = re.split('\s+', val)  #空格匹配
                            where["$and"] = []
                            for temp_i in temp:
                                where["$and"].append({ "org_name": {"$regex": re.compile("{0}".format(temp_i))} })
                        continue
                        parttern = re.compile("{0}".format(val))
                        where.update({
                            key:{"$regex": parttern}
                        })

        if params.get("unite_credict_code"):
            where = {
                "$or": [
                    {
                        "unite_credict_code":  params.get("unite_credict_code")
                    },
                    where
                ]
            }
        # print(where)
        collection =  Dossiers._get_collection()
        Societys_collection = Societys._get_collection() 
        page = params.get("page")
        limit = params.get("limit")
        work_range_count = 0
        if where  == {}:
            abort(400, **{"message":{"must":"请至少提供一个参数"}})
        res = Societys_collection.aggregate([
            {"$match": where},
            {   
                
                "$addFields":{
                    "name_score":{ "$cond": [  "$org_name", {"$divide":[ org_name_len, {"$strLenCP":"$org_name"}] }, 0 ]},
                    "law_men_score": { "$cond": [ {"$in": [ { "$indexOfCP":[ "$law_men" ,  params.get("law_men") ]}, [None, -1] ]} ,  0,  {"$divide":[ len(params.get("law_men", "")), {"$strLenCP":"$law_men"}] } ]},
                    "region_score": { "$cond": [{"$in": [  params.get("region"),  [ [], ['']]   ]} , 0, 1 ]},
                    "timerange_score": { "$cond": [ {"$in": [ params.get("timerange"),  [ [], ['']]   ]},  0,  1 ]},
                    "work_range_score": { "$cond": { "if" : bool(params.get("work_range")) , "then": 1, "else": 0 } },
                    "unite_credict_code_score": { "$cond": [ {"$eq": [ params.get("unite_credict_code",False),    "$unite_credict_code" ] } , 1, 0 ] },
                    "society_id": {
                        "$toString":"$_id"
                    },
                }
            },
            {
                "$addFields":{
                    "name_score_rate": {"$multiply": [ "$name_score",  weights.get("org_name")]  }, 
                    "law_men_score_rate": {"$multiply": [ "$law_men_score",  weights.get("law_men")] },
                    "region_score_rate": {"$multiply": [ "$region_score",  weights.get("region")]  },  
                    "work_range_score_rate": {"$multiply": [ "$work_range_score",  weights.get("work_range")] },
                    "timerange_score_rate": {"$multiply": [ "$timerange_score",  weights.get("timerange")] },
                    "unite_credict_code_score_rate":"$unite_credict_code_score",
                    "f_name_score_rate": {"$multiply": [ "$name_score",  weights_front.get("org_name")]  }, 
                    "f_law_men_score_rate": {"$multiply": [ "$law_men_score",  weights_front.get("law_men")] },
                    "f_region_score_rate": {"$multiply": [ "$region_score",  weights_front.get("region")]  },  
                    "f_work_range_score_rate": {"$multiply": [ "$work_range_score",  weights_front.get("work_range")] },
                    "f_timerange_score_rate": {"$multiply": [ "$timerange_score",  weights_front.get("timerange")] },
                }
            },
            {
                "$addFields":{
                    "score": { "$sum": [
                          "$name_score_rate", "$law_men_score_rate", "$region_score_rate", "$work_range_score_rate", "$timerange_score_rate", "$unite_credict_code_score_rate"
                        ]
                    },
                    "f_score": { "$sum": [
                          "$f_name_score_rate", "$f_law_men_score_rate", "$f_region_score_rate", "$f_work_range_score_rate", "$f_timerange_score_rate", "$unite_credict_code_score_rate"
                        ]
                    }
                }
            },
            {
                "$facet":{
                    "total":[
                        {"$count": "total" }
                    ],
                    "data": [
                        {
                            "$project":{
                                "_id": 0,
                            }
                        },
                        {
                            "$sort": {
                                "score": -1
                            }
                        },
                        {
                            "$skip": (page-1)*limit
                        },
                        {
                            "$limit": limit
                        },
                        
                    ]
                },
            },
            {
                "$project":{
                    "total": { 
                        "$arrayElemAt": [ "$total.total", 0 ] 
                    },
                    "data": 1
                }
            },

        ])
        society_data = loads(dumps(res))
        society_data  =  society_data[0] if len(society_data)>0 else {}
        return {
            "items": society_data,
            "code": 200,
            "returnToken": returnToken
        }
    def post(self, returnToken=None, userId=None):  #匹配微信
        params = self.parser.parse_args()
        where = {}
        weights_obj  = cal_weights()
        weights = weights_obj.get("weights", ['org_name', 'work_range', 'timerange'] )
        weights_front  = self.generateWeights(weights, filter_keys=['org_name'])
        org_name_len = 0
        for  key, val in params.items():
            if not val:
                continue

            if key == 'timerange':
                if val:
                    if len(val) == 2:
                        where.update({
                            "info.company_create_date":{"$gte": val[0], "$lte":val[1] },
                        })
                    elif len(val) == 1:
                        where.update({
                            "info.company_create_date":{"$gte": val[0] },
                        })
                else:
                    continue
            else:
                if key == "unite_credict_code":
                    continue
                if key!= "page" and key!="limit": 
                    val = val.strip()
                    if val:
                        if key == "org_name":
                            org_name_len = len(val.replace(" ",""))
                            temp = re.split('\s+', val)  #空格匹配
                            where["$and"] = []
                            for temp_i in temp:
                                # print(temp_i)
                                where["$and"].append({ "NickName": {"$regex": re.compile("{0}".format(temp_i)) } })
                            continue
                        if key == "work_range":
                            val = "|".join(jieba.lcut(val))
                            where.update({
                                "$or": []
                            })
                            where["$or"] =  where["$or"] + [ { "info.work_range_common": re.compile( "{0}".format(val) )  }, { "info.work_range_front_premit": re.compile("{0}".format(val) ) }]

        if params.get("unite_credict_code"):
            where= {
                "$or": [
                    {
                        "gs_credict_code":  params.get("unite_credict_code")
                    },
                    {
                        "zz_credict_code":  params.get("unite_credict_code")
                    },
                    where
                ]
            }
        if where  == {}:
            abort(400, **{"message":{"must":"请至少提供一个参数"}})

        page = params.get("page")
        limit = params.get("limit")
        source_collecion = Source._get_collection()
        res =  source_collecion.aggregate([
            {"$match": where},
            {
                "$facet":{
                    "total":[
                        {"$count": "total" }
                    ],
                    "data": [
                        {
                            "$project":{
                                "_id": 1,
                                "NickName": 1,
                                "info": {"$ifNull": ["$info", {}]},
                                "__biz": 1,
                                "name_score_one": 1,
                                "name_score_one":{ "$cond":[
                                        { "$and": ["$NickName", bool(params.get("org_name")) ] },
                                        {"$divide":[ org_name_len, {"$strLenCP": "$NickName" } ] },
                                        None,
                                    ]
                                },
                                "name_score_two":{ "$cond":[
                                        { "$and": ["$info.full_name", bool(params.get("org_name")) ] },
                                        {"$divide":[ org_name_len, {"$strLenCP": "$info.full_name" } ] },
                                        None,
                                    ]
                                },
                                "work_range_score": { "$cond": { "if" : bool(params.get("work_range")) , "then": 1, "else": 0 } },
                                "timerange_score": { "$cond": { "if" : bool(params.get("timerange")) , "then": 1, "else": 0 } },
                                "unite_credict_code_score": { "$cond": { "if" : bool(params.get("unite_credict_code")) , "then": 1, "else": 0 } },
                            }
                        },
                        {
                            "$addFields": {
                                "name_score":  {
                                    "$let":{
                                        "vars": {
                                            "name_score": "$name_score_one" or "$name_score_two" or 0
                                        },
                                        "in": "$$name_score"
                                    }
                                
                                },
                                "source_id": {
                                    "$toString":"$_id"
                                },
                            }
                        },
                        {
                            "$addFields": {
                                "name_score_rate": {"$multiply": [ "$name_score",  weights.get("org_name")]  }, 
                                "work_range_score_rate":{"$multiply": [ "$work_range_score",  weights.get("work_range")] },
                                "timerange_score_rate":{"$multiply": [ "$timerange_score",  weights.get("timerange")] },
                                "unite_credict_code_score_rate":"$unite_credict_code_score",
                                "f_name_score_rate": {"$multiply": [ "$name_score",  weights_front.get("org_name")]  }, 
                                "f_work_range_score_rate":{"$multiply": [ "$work_range_score",  weights_front.get("work_range")] },
                                "f_timerange_score_rate":{"$multiply": [ "$timerange_score",  weights_front.get("timerange")] },
                            }
                        },
                        {
                            "$addFields": {
                                "score": { "$sum": ["$name_score_rate", "$work_range_score_rate","timerange_score_rate", "$unite_credict_code_score_rate"]},
                                "f_score": { "$sum": ["$f_name_score_rate","f_timerange_score_rate", "$f_work_range_score_rate", "$unite_credict_code_score_rate"]}
                            }
                        },
                        {
                            "$sort": {
                                "score": -1
                            }
                        },
                        {
                            "$skip": (page-1)*limit
                        },
                        {
                            "$limit": limit
                        },
                        
                    ]
                },
            },
            {
                "$project":{
                    "total": { 
                        "$arrayElemAt": [ "$total.total", 0 ] 
                    },
                    "data": 1
                }
            },

        ])
        source_data = loads(dumps(res))
        source_data  =  source_data[0] if len(source_data)>0 else {}
        return {
            "items": source_data,
            "code": 200,
            "returnToken": returnToken
        }
        # res = cal_weights()
        # weights = res["weights"]
        # weights["社会组织名称"]  = weights.pop("org_name")
        # weights["统一社会信用代码"]  =  1
        # weights["法定代表人姓名"]  = weights.pop("law_men")
        # weights["行政区划"]  = weights.pop("region")
        # weights["业务范围"]  = weights.pop("work_range")
        # weights["成立登记日期"]  = weights.pop("timerange")
        # return {
        #     "data": res,
        #     "code": 200,
        #     "returnToken": returnToken
        # }
