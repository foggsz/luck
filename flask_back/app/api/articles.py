# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from app.models import Source, ArticleList, ArticleDetail
from bson.json_util import  dumps, ObjectId, loads 
# from bson.json_util import loads as bason_loads
from json import loads
from app.auth import verify_token
from datetime import datetime
from pymongo import DESCENDING, ASCENDING
import time

class ArticleLists(Resource):
    
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('limit', type=int, default=10)
        self.parser.add_argument('keyword', type=str, default='')
        self.parser.add_argument('timerange', type=int,  action="append", default=[])
        self.parser.add_argument('biz_id', type=str,  default='')

    decorators = [verify_token]
    def get(self, returnToken=None, userId=None):
        collection = ArticleList._get_collection()
        db = ArticleList._get_db()
        params = self.parser.parse_args()
        page  = params.get("page")
        limit = params.get("limit")
        keyword = params.get("keyword")
        timerange = params.get("timerange")
        biz_id = params.get("biz_id")
        biz_id = '^[\w\W]*' if biz_id == '' else   biz_id
        def sourceFuc():
            where = {}
            if len(timerange) == 2:
                where.update({
                    "pub_time" :{
                        "$gte": timerange[0],
                        "$lte": timerange[1]

                    }
                }) 
            articles = collection.find(where).sort([
                ('pub_time', DESCENDING)
            ]).skip((page-1)*limit).limit(limit)
            articles = list(articles)
            articles = loads(dumps(articles))
            total = collection.find(where).count()
            biz_ids  =  [ item.get("biz_id") for item in articles  if item.get("biz_id") ]
            sources = Source.objects.filter(__raw__={
                "__biz": {
                    "$in":biz_ids
                }
            }).exclude("_id").to_json()
            sources = loads(sources)
            for item in articles:
                for  item1 in sources:
                    if item.get("biz_id") == item1.get("__biz"):
                        item.update({
                            "extra": item1
                        })
            resData = {
                "data": articles,
                "total": total
            }
            return {
                "items": resData,
                "code": 200,
                "returnToken": returnToken
            }
        if keyword == '' and biz_id == '^[\w\W]*':
            return sourceFuc()
        else: 
            match_where_keyword = {
                "$match": {
                    "$and": [
                        {
                            "biz_id":{
                                        "$regex": biz_id, "$options":"i"
                                    }
                        },
                        {
                            "$or":[  
                                    {
                                        "biz_id": {"$regex":keyword, "$options":"i"}
                                    },
                                    {
                                        "title": {"$regex":keyword, "$options":"i"}
                                    },
                                    # {
                                    #     "extra": {
                                    #         "$elemMatch":{
                                    #             "NickName":{
                                    #                 "$regex":keyword, "$options":"i"
                                    #             }
                                    #         }
                                    #     }
                                    # },
                            ]
                        }
                    ]
                }
            }
        if len(timerange) == 2:
            match_where_keyword["$match"].update({
                "pub_time" :{
                    "$gte": timerange[0],
                    "$lte": timerange[1]

                }
            }) 
        piplelines = [
            {
                "$sort":{
                    "pub_time":-1
                }
            },
            match_where_keyword,
            {
                "$lookup":{
                    "from": "source",
                    "let": {'biz_id': "$biz_id"},
                    "pipeline": [
                        { "$match":
                            { "$expr":
                                { "$and":
                                    [
                                        { "$eq": [ "$__biz",  "$$biz_id" ] }
                                    ]
                                },
                            }
                        },
                    ],
                    # "localField": "biz_id",
                    # "foreignField": "__biz",
                    "as": "extra"
                },
            },
            {
                "$unwind":"$extra"
            },
            {
                "$facet":{
                    "total":[
                        {"$count": "total" }
                    ],
                    "data": [
                        {
                            "$skip": (page-1)*limit
                        },
                        {
                            "$limit": limit
                        },
                        {
                            "$project":{
                                "title":1,
                                "cover":1,
                                "author":1,
                                "pub_time":1,
                                "updateAt":1,
                                "extra.NickName": 1,
                                "extra.__biz":1,
                                "biz_id":1
                            }
                        }
                        
                    ]
                },
            },
            {
                "$project":{
                    "total": { 
                        "$arrayElemAt": [ "$total.total", 0 ] 
                    },
                    "data":1
                }
            }
        ]
        start = time.perf_counter()
        resData = collection.aggregate(piplelines)
        resData = loads( dumps(resData) )
        #print( db.command("aggregate", "article.list", pipeline=piplelines, explain=True) )

        if len(resData) == 0:
            resData = {
                "data": [],
                "total": 0
            }
        else:
            resData = resData[0]
        return {
            "items": resData,
            "code": 200,
            "returnToken": returnToken
        }
    
    def post(self, returnToken=None, userId=None):   #输入建议
        params = self.parser.parse_args()
        keyword = params.get("keyword")
        keyword = keyword.replace(" ",'')
        biz_id = params.get("biz_id")
        if keyword!='':
            if biz_id!='':
                suggests = ArticleList.objects.filter(__raw__={
                    "title": {"$regex":keyword, "$options":"i"},
                    "biz_id": biz_id
                }).only('title').exclude('_id').to_json()
                suggests = loads(suggests)  
            else:
                suggests = ArticleList.objects.filter(__raw__={
                    "title": {"$regex":keyword, "$options":"i"}
                }).only('title').exclude('_id').to_json()
                suggests = loads(suggests)  
        else:
            suggests = []
        return {
            "code": 200,
            "suggestions": suggests,
            "returnToken": returnToken
        }
    
class  ArticleDetails(Resource):
    decorators = [verify_token]
    def __init__(self, ):
        self.parser = reqparse.RequestParser()

    def get(self, article_id, returnToken=None, userId=None):
        article_id =  ObjectId(article_id)
        try:
            resData = ArticleDetail.objects.get(list_id = article_id).to_json()
        except Exception as e:
            resData = False
        return {
            "code": 200,
            "item": resData,
            "returnToken": returnToken
        }
    
    def post(self, article_id, returnToken=None, userId=None):           #articel ID 为列表文章ID
        now_timestamp = int(datetime.now().timestamp()*1000)
        self.parser.add_argument('title', type=str, required=True, help="标题不能为空")
        self.parser.add_argument('author', type=str, required=True, help="作者不能为空")
        self.parser.add_argument('content', type=str, required=True, help="内容不能为空")
        self.parser.add_argument('pub_time', type=int, help="类型错误", default=now_timestamp)
        self.parser.add_argument('content_url', type=str, help="类型错误")
        self.parser.add_argument('importance', type=int, help="类型错误")
        self.parser.add_argument('image_paths', type=list, default=[], help="类型错误")
        self.parser.add_argument('image_urls', type=list,  default=[], help="类型错误")
        # print("一碗碗晚安安安")
        try:
            olddata = ArticleList.objects.get(_id=ObjectId(article_id)).to_json()
        except Exception as e:
            print(e)
            return {
                "message":  "非法文章"
            }, 400            
        params = self.parser.parse_args()
        params.update({
            "list_id": ObjectId(article_id),
            "biz_id": olddata.get("biz_id"),
            "updateAt": datetime.now()
        })
        params['list_id'] = ObjectId(article_id)
        try:
            ArticleDetail.objects(list_id = ObjectId(article_id) ).update_one(**params, upsert=True)
        except Exception as e:
            print(e)
    
        return {
            "code": 200,
            "returnToken": returnToken
        }

