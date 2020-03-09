from  run_spider import run_spider
from flask_restful import Resource, reqparse
import threading
from concurrent.futures import ThreadPoolExecutor
from flask import make_response, request
import asyncio
from multiprocessing import Process
import subprocess
import os
from app.main import socketio
from app.models import ArticleList, Source
import json
from  app.auth  import  verify_token
from  config import  RUN_SPIDER_PATH
class StartSpider(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        # self.parser.add_argument('token', type=str)
        self.parser.add_argument('keyword', type=str,  required=True, help="请填入关键词")
        self.parser.add_argument('condition', type=str, required=True, help="请选择一个条件")
        self.parser.add_argument('isLoadImage',required=True ,type=str,help="该参数必传")
        self.parser.add_argument('extra', action="append", default=None, help="请传入一个数组")
        
    decorators = [verify_token]
    def post(self, returnToken=None, userId=None, *args, **kws):
        post_data = self.parser.parse_args()
        post_data['isLoadImage'] = False if post_data['isLoadImage']== "false" or post_data['isLoadImage']== "" else True
        post_data = json.dumps(post_data)
        cmd =['python', RUN_SPIDER_PATH, post_data]
        subprocess.Popen(cmd)
        return {
            "code": 200,
            "message": "任务已经开始",
            "returnToken": returnToken
        }
    
class StartSpiderOrg(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('org_type', type=str, required=True, help="请选择收集类型")
        self.parser.add_argument('goto_page',required=True ,type=int,  default=1)
        self.parser.add_argument('extra', action="append", default=None, help="请传入一个数组")
        
    decorators = [verify_token]
    def post(self, returnToken=None, userId=None, *args, **kws):
        post_data = self.parser.parse_args()
        post_data.update({
            "spiderName": "society"
        })
        post_data = json.dumps(post_data)
        cmd =['python', RUN_SPIDER_PATH, post_data]
        subprocess.Popen(cmd)
        return {
            "code": 200,
            "message": "任务已经开始",
            "returnToken": returnToken
        }

class StartSpiderGSL(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('rules', type=str, help="请传入字符串")
        self.parser.add_argument('start_url', type=str, help="请传入字符串")
        self.parser.add_argument('extra', action="append", default=None, help="请传入一个数组")
        
    decorators = [verify_token]
    def post(self, returnToken=None, userId=None, *args, **kws):
        post_data = self.parser.parse_args()
        post_data = dict( filter(lambda x: x[1], post_data.items()) )
        post_data.update({
            "spiderName": "gsl"
        })
        post_data = json.dumps(post_data)
        cmd =['python', RUN_SPIDER_PATH, post_data]
        subprocess.Popen(cmd)
        return {
            "code": 200,
            "message": "任务已经开始",
            "returnToken": returnToken
        }