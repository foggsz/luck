
from datetime import timedelta
import os
class Config(object):
    DEBUG = True
    TESTING = False
    # SECRET_KEY = b'g4w4ePhtSTLQ3roumCzQbamG'
    # SESSION_PERMANENT = False
    # PERMANENT_SESSION_LIFETIME = timedelta(seconds=10)
    # ALLOWED_EXTENSIONS = set(['txt', 'pdf'])
    # UPLOAD_FOLDER = "./upload"
    # MAX_CONTENT_LENGTH = 16 * 1024 * 1024
class DevelopmentConfig(Config):
    pass


if os.environ.get("flask_env")  == 'develop':
    BASE_URL = "http://localhost:8000/"
    ENV = "develop"
else:
    BASE_URL = "https://wx.hnzhixi.com/"
    # BASE_URL = "http://60.205.225.89:8001/"
    ENV = "product" 
UPLOAD_FOLDER = "upload"
UPLOAD_FOLDER_SHOW = "../upload/"
RUN_SPIDER_PATH = os.getcwd()+"/run_spider.py"