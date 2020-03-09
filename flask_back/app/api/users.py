from  flask_restful import Resource, reqparse
from  app.utils import verifyPass, verifyRoles
from  app.auth  import auth, verify_token, log_out_token
from  app.models  import Users
from bson.json_util import ObjectId
from datetime import datetime,timedelta

class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, help="用户名不能为空")
        self.parser.add_argument('password', type=str, required=True, help="密码不能为空")
    
    def post(self,):
        userData = self.parser.parse_args()
        result, msg, userId = verifyPass(**userData)
        if  not verifyRoles(userId, "admin"):
            return {
                "message": "你没有权限进入"
            },400
        if  result:
            if userData.get('username') == 'spider_admin':
                token = auth.create_token(**{"userId":  userId, 'exp': datetime.utcnow() + timedelta(days=30) })
            else:
                token = auth.create_token(**{"userId":  userId})
            return {
                "code": 200,
                "token": token
            }
        else:
            return {
                "message":msg
            },400

class LogOut(Resource):
    def post(self, ):
        return log_out_token()

class UserInfo(Resource):
    def __init__(self,):   
        self.parser = reqparse.RequestParser()
    decorators = [verify_token]
    def get(self, returnToken=None, userId=None):
        userData = Users.objects.only("roles").exclude("_id").get(_id=ObjectId(userId)).to_json()
        return {
            "code": 200,
            "returnToken": returnToken,
            "userData":userData
        }
