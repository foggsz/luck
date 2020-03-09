from mongoengine import *
from config import ENV
from sshtunnel import SSHTunnelForwarder
HOST = "47.104.150.23"
SSH_KEY = "/Users/pingguo1zhixi/.ssh/id_rsa"
# if ENV == "develop":
#     server = SSHTunnelForwarder(
#             (HOST, 22),
#             ssh_username="root",
#             ssh_pkey = SSH_KEY,
#             remote_bind_address=('127.0.0.1', 27017)
#         )
#     server.start()
#     connect('weixin', host="127.0.0.1", port=server.local_bind_port)
# else:
#     connect('weixin', host='localhost', port=27017)

connect('weixin', host='localhost', port=27017)
# connect('weixin', host='localhost', port=27017)
from datetime import datetime
from json import loads
from bson import json_util
from  config  import BASE_URL

class AwesomerQuerySet(QuerySet):
    def to_json(self, *args, **kwargs):
        """Convert this document to JSON.
        :param use_db_field: Serialize field names as they appear in
            MongoDB (as opposed to attribute names on this document).
            Defaults to True.
        """
        use_db_field = kwargs.pop('use_db_field', True)
        return json_util.dumps(self.to_mongo(use_db_field), *args, **kwargs)
    

class Users(Document):
    meta = {
        "collection":"users",
    }
    _id  = ObjectIdField()
    username = StringField(required =True, max_length=200)
    roles = ListField(required = True, default=[])
    password =  DictField(required = True)
    createAt =  DateTimeField(required=True, default=datetime.utcnow())
    updateAt =  DateTimeField(required=True, default=datetime.utcnow())
    avatar =  StringField(required=True, default=BASE_URL+"upload/user.svg")
    def to_json(self, *args, **kwargs):
        use_db_field = kwargs.pop('use_db_field', True)
        res = json_util.dumps(self.to_mongo(use_db_field), *args, **kwargs)
        return loads(res)

class ArticleList(Document):
    meta = {
        "collection":"article.list",
        'index_background' : True ,
        'indexes': [
            {'fields': ['-pub_time'] },
            {'fields': ['title','author', '-pub_time'] },
        ],
    }
    _id  = ObjectIdField()
    article_type = IntField()
    title =  StringField(max_length=50)
    cover =  StringField()
    content_url = StringField() 
    fileid = IntField()
    source_url = StringField()
    author = StringField()
    biz_id = StringField() 
    comm_msg_info = StringField()
    pub_time = LongField()
    createAt =  DateTimeField(required=True, default=datetime.utcnow())
    updateAt =  DateTimeField(required=True, default=datetime.utcnow())
    image_paths = ListField(default=[])
    image_urls = ListField(default=[])
    def to_json(self, *args, **kwargs):
        use_db_field = kwargs.pop('use_db_field', True)
        res = json_util.dumps(self.to_mongo(use_db_field), *args, **kwargs)
        return loads(res)


class ArticleDetail(Document):
    meta = {
        "collection":"article.detail",
    }
    _id  = ObjectIdField()
    title =  StringField(max_length=50)
    author = StringField(max_length=50)
    content = StringField()
    list_id = ObjectIdField()
    summary = StringField(max_length=50, default="")
    status = StringField(default="published") #文章发布状态
    importance = IntField(required=True, default=0) #文章重要性
    pub_time = LongField()
    image_urls = ListField(default=[])
    image_paths = ListField(default=[])
    content_url = StringField()
    biz_id = StringField() 
    createAt =  DateTimeField(required=True, default=datetime.utcnow())
    updateAt =  DateTimeField(required=True, default=datetime.utcnow())
    def to_json(self, *args, **kwargs):
        use_db_field = kwargs.pop('use_db_field', True)
        res = json_util.dumps(self.to_mongo(use_db_field), *args, **kwargs)
        return loads(res)


class Source(Document):
    meta = {
        "collection": "source",
        "strict": False
    }
    _id  = ObjectIdField()
    biz_id = StringField(db_field='__biz')
    appmsg_token = StringField()
    updateAt = DateTimeField()
    NickName = StringField()
    info   = DictField()
    tags = ListField()
    def to_json(self, *args, **kwargs):
        use_db_field = kwargs.pop('use_db_field', True)
        res = json_util.dumps(self.to_mongo(use_db_field), *args, **kwargs)
        print(res)
        return loads(res)

    
class  SpiderLogs(Document):
    meta = {
        "collection": "spider.logs",
        "strict": False
    }
    createAt = DateTimeField(required=True, default=datetime.utcnow())
    info =  StringField()
    status =  StringField()
    duration = IntField()
    keyword = StringField()

    def to_json(self, *args, **kwargs):
        use_db_field = kwargs.pop('use_db_field', True)
        res = json_util.dumps(self.to_mongo(use_db_field), *args, **kwargs)
        return loads(res)


class Tags(Document):
    meta = {
        "collection": "tags",
        "strict": False
    }
    _id  = ObjectIdField()
    createAt = DateTimeField(required=True, default=datetime.utcnow())
    value =  StringField()
    biz_id = ListField()
    def to_json(self, *args, **kwargs):
        use_db_field = kwargs.pop('use_db_field', True)
        res = json_util.dumps(self.to_mongo(use_db_field), *args, **kwargs)
        return loads(res)

class Societys(Document):
    _id  = ObjectIdField()
    org_name = StringField()     #组织名称
    unite_credict_code = StringField()  #统一社会组织代码
    register_organ = StringField()  #登记管理机关
    org_listener = StringField()   #业务主管机构
    law_men = StringField()           #法定代表人
    org_phone = StringField()          #联系电话
    register_founds = StringField()   #注册资金
    register_status = StringField()    #登记状态
    org_create_date = IntField()   #成立登记日期
    register_code = StringField()   #登记证号
    org_classify  = StringField()      #社会组织类型
    org_url = StringField()               #组织网址
    org_address = StringField()        #住所
    org_id =  StringField()           #组织ID  民政部登记有
    updateAt = DateTimeField()          #更新时间
    org_type = StringField()              #登记类型
    region = ListField()
    i  = StringField()               #地方登记有
    u  = StringField()               #地方登记有
    org_cert_expire  = ListField(required = True, default=[])    #证书有效期
    work_range = StringField()     #业务范围
    score = FloatField()
    org_tag  = ListField(required = True, default=[])      #组织标签
    meta = {
        "collection": "society",
        "strict": False,
        'index_background' : True ,
        'indexes': [
            # {'fields': 'org_name'},
            # {'fields': 'org_name'},
            # {'fields': 'org_name'},
            {'fields': ['law_men']},
            {'fields': ['org_classify']},
            {'fields': ['org_name']},
            {'fields': ['org_type']},
            {'fields': ['register_organ']},
            {'fields': ['org_listener']},
            {'fields': ['-org_create_date'] },
            {'fields': ['law_men', '-org_create_date'] },
            {'fields': ['org_name','register_organ','-org_create_date']},
            {'fields': ['org_name','law_men','-org_create_date']},
            {'fields': ['org_name','org_classify','-org_create_date']},
            {'fields': ['org_name','org_type','-org_create_date']},
            {'fields': ['org_name','-org_create_date'] },
            {'fields': ['org_tag','-org_create_date'] },
            {'fields': ['org_classify','-org_create_date'] },
            {'fields': ['org_type','-org_create_date']},
            {'fields': ['org_type', 'register_organ', 'org_listener', 'org_name', 'org_address','-org_create_date']},
            {'fields': ['register_status','-org_create_date'] },
            {'fields': ['region','-org_create_date'] },
            {'fields': ['-score','-org_create_date']},
            {'fields': ['unite_credict_code','-org_create_date']},
        ],
    }
 
    
    def to_json(self, *args, **kwargs):
        use_db_field = kwargs.pop('use_db_field', True)
        res = json_util.dumps(self.to_mongo(use_db_field), *args, **kwargs)
        return loads(res)

class Migrates(Document):
    meta = {
        "collection": "migrates",
        "strict": False
    }
    _id  = ObjectIdField()
    version = IntField()     #版本号
    comment = StringField()  #解释说明
    lock = BooleanField     #锁定


class  Dossiers(Document):     #档案表
    meta = {
        "collection": "dossiers",
        'strict': False ,
        'index_background' : True ,
        'indexes': [
            {'fields': ['-org_create_date'] },
            {'fields': ['law_men','-org_create_date'] },
            {'fields': ['org_name','-org_create_date'] },
            {'fields': ['org_classify','-org_create_date'] },
            {'fields': ['society_ids','-org_create_date'] },
            {'fields': ['source_ids','-org_create_date'] },
            {'fields': ['unite_credict_code','-org_create_date']},
            {'fields': ['society_ids._id','-org_create_date']},
            {'fields': ['society_ids.org_name','-org_create_date']},
            {'fields': ['society_ids.f_score','-org_create_date']},
            {'fields': ['source_ids._id','-org_create_date']},
            {'fields': ['source_ids.org_name','-org_create_date']},
            {'fields': ['source_ids.f_score','-org_create_date']},
        ],
    }

    _id  = ObjectIdField() 
    unite_credict_code = StringField()
    org_name = StringField()
    law_men = StringField()
    org_create_date = IntField()   #成立登记日期
    work_range = StringField()
    region = ListField()
    org_classify = StringField()
    logo_url = StringField()   #Logo地址
    society_ids = ListField()   #社会组织ID
    source_ids = ListField()    #微信ID
    extra =  StringField()   #其他信息
    createAt =  DateTimeField(required=True, default=datetime.utcnow())
    updateAt =  DateTimeField(required=True, default=datetime.utcnow())

    def to_json(self, *args, **kwargs):
        use_db_field = kwargs.pop('use_db_field', True)
        res = json_util.dumps(self.to_mongo(use_db_field), *args, **kwargs)
        return loads(res)

class  ExpireLogs(Document):     #有时间限制的表
    _id = ObjectIdField()
    createAt = DateTimeField(required=True, default=datetime.utcnow())
    info =  StringField()
    status = StringField()
    classify = StringField()
    biz_id = StringField()
    meta = {
        "collection": "expire.logs",
        "strict": False,
        'index_background' : True ,
        'indexes': [        
            {'fields': ['createAt'], 'expireAfterSeconds': 60*60*24} ,
        ],
    }

    def to_json(self, *args, **kwargs):
        use_db_field = kwargs.pop('use_db_field', True)
        res = json_util.dumps(self.to_mongo(use_db_field), *args, **kwargs)
        return loads(res)


class GSL(Document):     #有时间限制的表
    _id = ObjectIdField()
    gsl_name = StringField()         #名字
    gsl_sub = StringField()          #简介
    category = StringField()         #抓取的栏目
    title  = StringField()           #文章标题
    pub_time = LongField()          #发布时间
    source  = StringField()         #文章来源
    summary =  StringField()        #文章简介
    content =  StringField()        #文章来源
    region =  ListField()           #工商联所属地区
    net_address = StringField()     #工商网址
    detail_url = StringField()     #详情网址
    createAt = DateTimeField(required=True, default=datetime.utcnow(),)
    updateAt = DateTimeField()
    meta = {
        "collection": "gsl",
        "strict": False,
        'indexes': [
            {'fields': ['-updateAt'] },
            {'fields': ['-pub_time'] },
            {'fields': ['category']},
            {'fields': ['title', '-updateAt']},
            {'fields': ['category', '-updateAt']},
            {'fields': ['region', '-updateAt']},
            {'fields': ['title', 'category', 'region','-updateAt']},
            {'fields': ['title', '-pub_time']},
            {'fields': ['category', '-pub_time']},
            {'fields': ['region', '-pub_time']},
            {'fields': ['title', 'category', 'region','-pub_time']},
        ]
    }
    
    def to_json(self, *args, **kwargs):
        use_db_field = kwargs.pop('use_db_field', True)
        res = json_util.dumps(self.to_mongo(use_db_field), *args, **kwargs)
        return loads(res)