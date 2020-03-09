from flask_restful  import abort
def my_abort(http_response, *args, **kwargs):
    if http_response == 400:
        errmsg = kwargs.get('message',dict())
        for i in errmsg:
            errmsg = errmsg[i]
        
        errdata = {
            "message": errmsg,
            "fullMsg": kwargs.get('message',dict())
        }
        return abort(http_response, **errdata)
    return abort(http_response, **kwargs)