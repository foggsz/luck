from flask import Flask, render_template, request, redirect, url_for, g
import re
from flask_cors import CORS
import app.migrate 
import flask_restful
from app.errors import my_abort
flask_restful.abort = my_abort
from flask_restful import Api
from flask_socketio import SocketIO, emit, send, join_room, leave_room
app = Flask(__name__, template_folder='../../vue_front/dist', static_folder='../../vue_front/dist/static')
app.config.from_object('config.DevelopmentConfig')
CORS(app, resources={r"*": {"origins": "*"}})
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def call_routh_path(path):
    return render_template("index.html")
socketio = SocketIO(app, async_mode='gevent', message_queue='redis://localhost:6379/0')
api = Api(app)

from app.api.users import *
from app.api.articles import *  
from app.api.spider import *
from app.api.upload import *
from app.api.resources import *
from app.api.sources  import *
from app.api.logs  import *
from app.api.tags  import *
from app.api.society  import *
from app.api.dossiers  import *
from app.api.gsl  import *
import time

@app.after_request
def after_request(response):
    # response.headers.add('Access-Control-Allow-Credentials', 'true')   #跨域
    return response

def init_api():
    api.add_resource(Login, "/api/user/login")
    api.add_resource(LogOut, "/api/user/logout")
    api.add_resource(Upload, "/api/upload")
    api.add_resource(GetResources, "/upload/<path:pathname>")
    api.add_resource(UserInfo, "/api/user/info")
    api.add_resource(WxSource, "/api/wx/source")
    api.add_resource(WxSourceUrl, "/api/wx/sourceurl")
    api.add_resource(StartSpider, "/api/wx/spider")
    api.add_resource(StartSpiderOrg, "/api/wx/spiderorg")
    api.add_resource(StartSpiderGSL, "/api/wx/spidergsl")
    api.add_resource(ArticleLists, "/api/article/list")
    api.add_resource(ArticleDetails, "/api/article/<string:article_id>")
    api.add_resource(SpiderLog, "/api/logs/spider")
    api.add_resource(Tag, "/api/tags")
    api.add_resource(Society, "/api/society")
    api.add_resource(DossierMatch, "/api/dossier/match")
    api.add_resource(Dossier, "/api/dossier")
    api.add_resource(GSLAPI, "/api/gsl")

init_api()