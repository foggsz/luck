from flask_restful import Resource, reqparse
from app.models import Societys
from app.auth import verify_token
from json import loads
from datetime import datetime, time
from app.utils import search_city
from bson.json_util import  dumps, ObjectId 
from pymongo import DESCENDING, ASCENDING
import re
import time
class Society(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('limit', type=int, default=10)
        self.parser.add_argument('org_name', type=str, help="请传入字符串类型")
        self.parser.add_argument('unite_credict_code', type=str, help="请传入字符串类型")
        self.parser.add_argument('law_men', type=str, help="请传入字符串类型")
        self.parser.add_argument('register_status', type=str, help="请传入字符串类型")
        self.parser.add_argument('register_organ', type=str, help="请传入字符串类型")
        self.parser.add_argument('org_listener', type=str, help="请传入字符串类型")
        self.parser.add_argument('org_classify', type=str, help="请传入字符串类型")
        self.parser.add_argument('org_type', type=str, help="请传入字符串类型")
        self.parser.add_argument('org_tag', type=str, action="append",help="请选择标签", default=[])
        self.parser.add_argument('timerange', type=int,  action="append", default=[])
        self.parser.add_argument('region', type=str,  action="append", default=[])
        self.parser.add_argument('society_id', type=str)
    decorators = [verify_token]
    def get(self, returnToken=None, userId=None):
        where = {}
        params = self.parser.parse_args()
        page = params.get("page")
        limit = params.get("limit")
        org_name = params.get("org_name")
        temp_params  = list(params.items())
        society_id  = params.get("society_id")
        if society_id:
            res= Societys.objects.get(_id=ObjectId(society_id)).to_json()
            return {
                "data": res,
                "code": 200,
                "returnToken": returnToken
            }
        for item in params.items():
            key, val = item
            if val:
                if key== "page" or key== "limit": 
                    continue
                if key == "timerange" and val:
                    where.update({
                        "org_create_date": {
                            "$gte": val[0],
                            "$lte": val[1]
                        }
                    })
                elif key == "org_tag":
                    where.update({
                        "org_tag": {"$all": val}
                    })
                elif key == "region":
                    where.update({
                        "region":{"$all": val},
                    })
                else:
                    if val:
                        if key  in ['org_classify', 'register_status', 'org_type'] :
                            if val == "全部":
                                continue
                            else:
                                where.update({
                                    key:val
                                })
                        else:
                            val = re.compile(val)
                            where.update({
                                # key:val,
                                key: {
                                    "$regex": val,
                                    "$options": "i"
                                }
                            })
        if where == {}:
            total = Societys.objects.filter(__raw__=where).count()
            res = Societys.objects.filter(__raw__=where).order_by("-org_create_date").skip((page-1)*limit).limit(limit).to_json()   
            res =  loads(res)
            res = {
                "total": total,
                "data": res
            }
            return {
                "items": res,
                "code": 200,
                "returnToken": returnToken
            }

        pipeline = [
            {"$match": where},
            {"$sort":{
                "org_create_date": -1
                }
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

                    ],

                }
            },
            {
                "$project":{
                    "total": { 
                        "$arrayElemAt": [ "$total.total", 0 ] 
                    },
                    "data": 1
                }
            },
        ]
        res = Societys.objects.aggregate(*pipeline)
        res = loads(dumps(res))
        res = res[0] if len(res)>0 else {}
        return {
            "items": res,
            "code": 200,
            "returnToken": returnToken
        }
