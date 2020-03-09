from flask_restful import Resource, reqparse
from app.auth  import  verify_token
from bson.json_util import  dumps, ObjectId
from json import loads
from app.models import Source, ExpireLogs
from datetime import datetime
class WxSource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('limit', type=int, default=10)
        self.parser.add_argument('keyword', type=str, help="请传入字符串类型")
        self.parser.add_argument('tags', type=str, action="append",help="请传入组织标签")
        self.parser.add_argument('source_id', type=str,)
    decorators = [verify_token]
    def get(self, returnToken=None, userId=None):
        collection = Source._get_collection()
        # collection.create_index([("updateAt",-1)])
        params = self.parser.parse_args()
        page  = params.get("page")
        limit = params.get("limit")
        tags = params.get("tags")
        keyword = params.get("keyword")
        source_id = params.get("source_id")
        if source_id:
            res = Source.objects.get(_id=ObjectId(source_id)).to_json()
            return {
                "code": 200,
                "items":resData,
                "returnToken": returnToken
            }
        where = { "$or": [ {"NickName": {"$regex": keyword,"$options":"i"}}, {"__biz": {"$regex": keyword,"$options":"i"}} ]} if keyword else {}
        if tags and len(tags) >0 :
           where.update({
               "tags": {
                   "$all": tags
               }
           })
        resData = collection.aggregate([
            {
                "$match": where
            },
            {   "$lookup":{
                    "from": "article.list",
                    "let":  {"sourceId": "$__biz"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {  
                                    "$eq":["$biz_id" ,"$$sourceId"]
                                    }
                            }
                        },
                        {
                            "$count": "article_count"
                        }

                    ],
                    "as": "count"
                }
                
            },
            {
                "$facet": {
                    "total": [
                      {"$count": "total"}  
                    ],
                    "data":[
                        # {
                        #     "$match": where
                        # },
                        # { 
                            # "$lookup":{
                            #     "from": "article.list",
                            #     "localField": "__biz",
                            #     "foreignField": "biz_id",
                            #     "as": "count"
                            # }
                        #    "$lookup":{
                        #         "from": "article.list",
                        #         "let":  {"sourceId": "$__biz"},
                        #         "pipeline": [
                        #             {
                        #                 "$match": {
                        #                     "$expr": {  
                        #                         "$eq":["$biz_id" ,"$$sourceId"]
                        #                         }
                        #                 }
                        #             },
                        #             {
                        #                 "$count": "article_count"
                        #             }
  
                        #         ],
                        #         "as": "count"
                        #     }
                        # },
                        {
                            "$unwind": {
                               "path": "$count",
                               "preserveNullAndEmptyArrays": True
                            }
                        },
                        {
                            "$project" : {
                                "updateAt": 1,
                                "NickName": 1,
                                "__biz": 1,
                                "info": {
                                    "$ifNull":[
                                        "$info",
                                        {}
                                    ]
                                },
                                "tags": {
                                    "$ifNull":[
                                        "$tags",
                                        []
                                    ]
                                },
                                "article_count": {
                                    "$ifNull": [
                                        "$count.article_count",
                                        {"$literal": 0}
                                    ]
                                }
                            }
                        },
                        {
                            "$sort": {
                                "updateAt": -1
                            }
                        },
                        {
                            "$skip": (page-1)*limit
                        },
                        {
                            "$limit": limit
                        },
                    ]
                }
            },
            {
                "$project": {
                    "total": {
                        "$arrayElemAt": [ "$total.total", 0 ] 
                    },
                    "data": 1
                }
            }



        ])
        resData = loads( dumps(resData) )
        if len(resData) == 0:
            resData = {
                "data": [],
                "total": 0
            }
        else:
            resData = resData[0]
        
        return {
            "code": 200,
            "items":resData,
            "returnToken": returnToken
        }
    
    def post(self, returnToken=None, userId=None):
        self.parser.add_argument('biz_id', type=str, help="请传入字符串类型")
        self.parser.add_argument('tags', type=str, action="append",help="请传入组织标签")
        params = self.parser.parse_args()
        biz_id = params.get("biz_id")
        tags = params.get("tags")
        resData = Source.objects.get(tags=tags).only("info").to_json()
        resData = loads(resData)
        return {
            "code": 200,
            "data":resData,
            "returnToken": returnToken
        }
    
class WxSourceUrl(Resource):
    decorators = [verify_token]
    def get(self, returnToken=None, userId=None):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('sourceId', type=str, default=None)
        self.parser.add_argument('limit', type=int, default=20)
        params = self.parser.parse_args()
        sourceId = params.get("sourceId")
        limit = params.get("limit")
        if sourceId:
            sourceId = ObjectId(sourceId)
            res = Source.objects.filter(__raw__=
                { "_id": {"$gt": sourceId } }
            ).only('_id', "biz_id").limit(limit).to_json()
        else:
            res = Source.objects.only('_id',"biz_id").limit(limit).to_json()
            
        res = loads(res)
        length = len(res)
        if length>0:
            failData = ExpireLogs.objects.filter(__raw__={"classify":"biz", "status":"fail", }).only('_id', "biz_id").limit(limit).to_json()
            failData = loads(failData)
            if len(failData) > 0 :
                failData[-1]["_id"]["$oid"] = res[-1]["_id"]["$oid"]
                res = res + failData
        for item in res:
            item.update({
                "url": "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={0}&scene=124#wechat_redirect".format(item.get("__biz"))
            })            
        return {
            "code": 200,
            "items": res,
            "returnToken": returnToken
        }

    def post(self, returnToken=None, userId=None):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('keyword', type=str, default=None)
        params = self.parser.parse_args()
        keyword = params.get("keyword")
        try:
            res = Source.objects.only('_id',"biz_id").get(NickName=keyword).to_json()
        except Source.DoesNotExist as e:
            res = None
        else:
            res.update({
                "url": "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={0}&scene=124#wechat_redirect".format(res.get("__biz"))
            })
        return {
            "code": 200,
            "data": res,
            "returnToken": returnToken
        }
