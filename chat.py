import os
from flask import Flask
from flask import Response
from flask import request
from flask import abort
from datetime import datetime
import moment
from flask_sockets import Sockets
from flask import Flask
import time
from flask_socketio import SocketIO, emit

app = Flask(__name__)
sockets = Sockets(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)

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

@app.route('/time')
def time():
   return moment.now().format("YYYY-M-D")

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

@socketio.on('connect', namespace='/chat')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    print('Client disconnected')
