from  flask_restful import Resource, reqparse
from  app.auth  import  verify_token
from app.models import Tags, Source
from datetime import datetime
from json import loads
class Tag(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    decorators = [verify_token]
    
    def get(self, returnToken=None, userId=None):
        resData = Tags.objects().only('value').to_json()
        resData = loads(resData)
        return {
            "code": 200,
            "items":resData,
            "returnToken": returnToken
        }

    def post(self, returnToken=None, userId=None):
        self.parser.add_argument('biz_id', required=True, type=str, help="请传入组织ID")
        self.parser.add_argument('tags', required=True, type=str, action="append",help="请传入组织标签")
        params = self.parser.parse_args()
        tags = params.get("tags")
        biz_id = params.get("biz_id")
        collection =  Source._get_collection()
        updateData = {
            "$addToSet": {
                "tags": {
                    "$each": tags
                }
            }
    
        }
        collection.update_one({"__biz":biz_id},updateData)
        insertData = {

        }
        tags_collection = Tags._get_collection()
        for val in tags:
            tags_collection.update_one(
                {
                    "value":val
                },
                {
                    "$set":{
                        "value":val
                    },
                    "$addToSet": {
                        "biz_id": biz_id,
                        "createAt": datetime.now()
                    }
                },
                upsert=True
            )

        return {
            "code": 200,
            "returnToken": returnToken
        }

    def delete(self, returnToken=None, userId=None):
        self.parser.add_argument('biz_id', required=True, type=str, help="请传入组织ID")
        self.parser.add_argument('tags', required=True, type=str, help="请传入组织标签")
        params = self.parser.parse_args()
        tags = params.get("tags")
        biz_id = params.get("biz_id")
        collection =  Source._get_collection()
        tags_collection = Tags._get_collection()
        delData = {
            "$pull": {
                "tags": tags
            }
    
        }
        collection.update_one({"__biz":biz_id},delData)
        tags_collection.update_one({"value": tags}, {
           "$pull": {
                "biz_id": biz_id
            } 
        })
        return {
            "code": 200,
            "returnToken": returnToken
        }