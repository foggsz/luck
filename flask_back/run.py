from gevent import monkey
monkey.patch_all()
from  app.main import app, socketio
# from  eventlet import monkey_patch
# import redis
# gevent.monkey.patch_all()
if __name__ == "__main__":
    socketio.run(app, port=8000, debug=True)
