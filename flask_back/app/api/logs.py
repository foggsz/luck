from flask_restful import Resource, reqparse
from app.models import SpiderLogs
from app.auth import verify_token
from json import loads
from datetime import datetime, time
class SpiderLog(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page', type=int, default=1)
        self.parser.add_argument('limit', type=int, default=10)
        self.parser.add_argument('keyword', type=str, default='^\w*')
        self.parser.add_argument('timerange', type=int, action="append", help="请传入正确的参数")
    
    decorators = [verify_token]
    def get(self, returnToken=None, userId=None):
        params = self.parser.parse_args()
        page  = params.get("page")
        limit = params.get("limit")
        keyword = params.get("keyword")
        timerange = params.get("timerange")
        # try:
        #     start = datetime.fromtimestamp(timerange[0]/1000)
        #     end = datetime.fromtimestamp(timerange[1]/1000)
        # except Exception as e:
        #     start = datetime.combine(datetime.now(), time.min)
        #     end = datetime.combine(datetime.now(), time.max)
        where = {
                "keyword": {
                    "$regex": keyword+'[^finished]',
                    "$options": "i"
                }
        }
        if timerange and len(timerange) == 2 :
            where.update({
                "createAt": {
                    "$gte": datetime.fromtimestamp(timerange[0]/1000),
                    "$lte": datetime.fromtimestamp(timerange[1]/1000)
                }
            })     
        total = SpiderLogs.objects(__raw__=where).count()
        resData = SpiderLogs.objects(__raw__=where).order_by('-createAt').skip((page-1)*limit).limit(limit).to_json()
        resData = loads(resData)
        return {
            "items": {
                "data": resData,
                "total": total
            },
            "code": 200,
            "returnToken": returnToken
        }
        