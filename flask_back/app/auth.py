import jwt
import sys
from datetime import datetime,timedelta
import redis
from flask_restful  import request
r = redis.StrictRedis(host='localhost', port=6379, db=0)
token_exp = timedelta( hours=2 )  #token过期时间
refresh_exp = timedelta(days=15) #第二个token过期时间

secert = 'asedsadsauihdsajkhdhqwuieqweqw87878784455523dsfsdfsdfdgtffghkllkl;lk23lk32jlkmlknxmlc,xmckxkxlcclksdkld2323;l;asadsadasqweqwewqeasdasdsadsadsad541345658798**122332a11/ s11iIcmkmvcvbjcvlnbdfsrf./aq.,,gdfgfdwerwqwe'
class Auth(object):     #登录创建Token
    def create_token(self, **preload):
        if not preload.get("exp"):
            preload.update({"exp": datetime.utcnow() + token_exp})
        jwt_token= jwt.encode( preload, secert , algorithm ='HS256').decode("utf-8")
        userId = preload.get("userId")
        r.set(userId, jwt_token)
        return jwt_token 
    
    def create_refresh_token(self, ):
        refresh_token = jwt.encode({"exp": datetime.utcnow() + refresh_exp },secert , algorithm ='HS256').decode("utf-8")
        return refresh_token

    def verify_token(self, token, refresh_token=None):
        try:
            preload = jwt.decode(token, secert, verify=True)
        except jwt.exceptions.ExpiredSignatureError:
            return False, 5003 , "登录过期"
        except  jwt.exceptions.DecodeError:
            return False, 5002 , "错误登录"
        else:
            redis_token = r.get(preload.get("userId"))
            # print(redis_token)
            # print(token)
            if redis_token and  token == redis_token.decode("utf-8"): 
                if datetime.now().timestamp() + 3600 >= preload.get('exp') and datetime.now().timestamp() <= preload.get('exp'):  #将旧的ROKEN  归入黑名单
                    returnToken = auth.create_token(**{ 
                        "userId":preload.get("userId")
                    })
                    # print("refresh")
                    # print("refresh", returnToken)
                    return  preload.get("userId"), 5004, returnToken
            else:
                # print("非法登录", token)
                return False, 5002 , "非法登录"
            
        return preload.get("userId"), 200, "登录成功"


        # if r.get(token):
        #     return False, 5003 , "登录失效"
        # else:
        #     try:
        #         preload = jwt.decode(token, secert, verify=True)
        #     except jwt.exceptions.ExpiredSignatureError:
        #         return False, 5003 , "登录过期"
        #     except  jwt.exceptions.DecodeError:
        #         return False, 5002 , "非法登录"
        #     else:
        #         if datetime.now().timestamp() + 3600 >= preload.get('exp') and datetime.now().timestamp() <= preload.get('exp'):  #将旧的ROKEN  归入黑名单
        #             residue_exp = preload.get('exp')  - int( datetime.now().timestamp() )
        #             r.setex(token, residue_exp, True)
        #             returnToken = auth.create_token(**{ 
        #                 "userId":preload.get("userId")
        #             })
        #             return  preload.get("userId"), 5004, returnToken

        #     return preload.get("userId"), 200, "登录成功"
    
    
    def log_out_token(self, token):
        preload = jwt.decode(token, secert, verify=False)
        # residue_exp = preload.get('exp')  - int( datetime.now().timestamp() )
        # r.setex(token, residue_exp, True)
        r.delete(preload.get("userId"))
        return True, 200, "注销成功"

auth = Auth()
def verify_token(f):
    """Checks whether user is logged in or raises error 401."""
    def decorator(*args, **kwargs):
        token = request.headers.get("authorization")
        if not token:
            return {
                "code": 5001,
                "message": "非法认证"
            }
        else:
            userId, code, message = auth.verify_token(token=token)
            if userId:
                if code == 5004:
                    return f(returnToken=message, userId=userId, *args, **kwargs)  
                return f(userId=userId, *args, **kwargs)
            
            return {
                "code": code,
                "message": message
            }
    return decorator

def log_out_token():
    token = request.headers.get("authorization")
    if not token:
        return {
            "code": 5001,
            "message": "非法认证"
        }
    else:
        res, code, message = auth.log_out_token(token=token)           
        return {
            "code": code,
            "message": message
        }
    
    