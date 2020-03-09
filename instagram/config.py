import os
class Config(object):
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.urandom(16)