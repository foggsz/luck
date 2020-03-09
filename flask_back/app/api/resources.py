from  flask_restful import Resource, reqparse, request
from  flask import send_from_directory
from  app.auth  import  verify_token
from  config import  UPLOAD_FOLDER_SHOW


class GetResources(Resource):
    def __init__(self,):   
        self.parser = reqparse.RequestParser()
    
    def get(self, pathname, returnToken=None, userId=None):
        return send_from_directory("../upload/", pathname, as_attachment=True)
        


