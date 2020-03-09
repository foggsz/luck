# -*- coding: utf-8 -*-
from  flask_restful import Resource, reqparse
from  app.auth  import  verify_token
import werkzeug
import os
from uuid import uuid1
from  config import BASE_URL, UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def upload_file(file ):
    name  =  file.filename.split(".")[0]
    folder=UPLOAD_FOLDER
    postfix = file.filename.split(".")[-1]
    if postfix not in ALLOWED_EXTENSIONS:
        return False, "文件类型不符合" , None
    name = str(uuid1(node=123456)).replace("-","") + '.'+ postfix
    if os.path.exists(folder):   
        fullname = os.path.join(folder, name)
    else:
        os.makedirs(folder)
        fullname = os.path.join(folder, name)
    file.save(fullname)
    return True,  "上传成功", BASE_URL+fullname

class Upload(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files',required=True, help="图片不能为空")
    
    decorators = [verify_token]
    def post(self, returnToken=None, userId=None):
        postdata = self.parser.parse_args()
        file = postdata.get("file")
        result, message, url = upload_file(file)
        return {
            "code": 200 ,
            "message": message,
            "returnToken": returnToken,
            "result":result,
            "url": url
        }
                   