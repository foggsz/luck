from flask import Flask,  send_from_directory
from flask_cors import CORS
app = Flask(__name__)
app.config.from_object("config.Config")
CORS(app, resources={r"*": {"origins": "*"}})


from index import index
app.register_blueprint(index)


@app.route("/video/<path:pathname>")
def video(pathname):
    return send_from_directory("video",  pathname,)

@app.errorhandler(Exception)
def special_exception_handler(error):
    err_msg = str(error)
    return  err_msg, 500

app.run(port=3000,debug=True)