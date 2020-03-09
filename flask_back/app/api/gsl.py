from flask_restful import Resource, reqparse
from app.models import GSL
from bson.json_util import  dumps, ObjectId, loads 
# from bson.json_util import loads as bason_loads
from json import loads
from app.auth import verify_token
from datetime import datetime
import time

class GSLAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('limit', type=int, default=10)
        self.parser.add_argument('title', type=str, default='')
        self.parser.add_argument('category', type=str, default='')
        self.parser.add_argument('region', type=str,  action="append", default=[])

    decorators = [verify_token]
    def get(self, returnToken=None, userId=None):
        params = self.parser.parse_args()
        page  = params.get("page")
        limit = params.get("limit")
        where = {}
        for key, val in params.items():
            if key== "page" or key== "limit": 
                continue
            if val:
                if key == "region":
                    where.update({
                        "region":{"$all": val},
                    })
                elif key == "category":
                    where.update({
                        "category": val,
                    })
                else:
                    where.update({
                        key:{ "$regex": val},
                    })
        total = GSL.objects.filter(__raw__=where).order_by("-pub_time").count()
        categorys = GSL.objects.all().distinct('category')
        data = GSL.objects.filter(__raw__=where).order_by("-pub_time").skip( (page-1)*limit ).limit(limit).to_json()
        data = loads(data)
        res = {
            "data": data,
            "total": total,
            "categorys": categorys
        }
        return {
            "items": res,
            "code": 200,
            "returnToken": returnToken
        }