from flask import Blueprint,render_template, request, flash, redirect, url_for, jsonify, Response, send_file
from utils.down import get_data
from io import BytesIO, StringIO
import base64
index = Blueprint('index', __name__,)
@index.route("/", methods=['GET', 'POST'])
def index_handle():
    args = dict(request.args)
    tag = args.get("tag", "img")
    if request.method == 'POST':
        try:
            data = request.json
            url = data.get("url")
            if url:
                res = get_data(**{"url": url, "tag":tag})
                if type(res) == dict:
                    return jsonify(res), 200
                return res

        except Exception as e:
            return jsonify({'status': "fail", "message": str(e) }), 200
    return render_template("index/index.html", tag=tag)


    
