import os
from flask import Flask
from flask import Response
from flask import request
from flask import abort
from datetime import datetime
import moment
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
socketio.run(app)

@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/env')
def env():
    html = "System Environment:\n\n"
    for env in os.environ.keys():
      html += env + ': ' + os.environ[env] + "\n"
    return Response(html, mimetype='text/plain')

@app.route('/user_log')
def post():
    with open("/home/vcap/fs/2ad834759b976e6/login.log","a+") as fo:
        fo.write(moment.now().format("YYYY-M-D"))
        fo.write("----")
        fo.write(request.args.get('info'))
        fo.write("\n")
    return request.args.get('info')

@socketio.on('connect')
def test_message(message):
    currentSocketId = request.namespace.socket.sessid
    print currentSocketId
    emit('my response', {'data': 'got it!'})