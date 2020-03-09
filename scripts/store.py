from json import dumps, loads
import os
default =  {"refresh_name" : None, "start_name": None,  "limit_name": None}
filename = "store.json"
# with open(filename, "w") as f:
#     str_default = dumps(default)
#     f.write(str_default)
def read():
    if os.path.exists(filename):
        with open(filename) as f:
            data = f.read()
            return loads(data)
    else:
        with open(filename, "w") as f:
            str_default = dumps(default)
            f.write(str_default)
            return default
    
def update(**kws):
    if os.path.exists(filename):
        with open(filename, 'r+') as f:
            data = f.read()
            data = loads(data)
            f.seek(0)
            f.truncate()
            data.update(kws)
            kws = dumps(data)
            f.write(kws)
            return data
    else:
        return default

def delete(key):
    if os.path.exists(filename):
        with open(filename, 'r+') as f:
            data = f.read()
            data = loads(data)
            res = data.pop(key, None)
            f.seek(0)
            f.truncate()
            kws = dumps(data)
            f.write(kws)
            return res
    else:
        return None