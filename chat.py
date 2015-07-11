import os
import redis
from flask import Flask
from flask import Response
from flask import request
from flask import abort
from datetime import datetime
import moment
from flask_sockets import Sockets
from flask import Flask
import time

app = Flask(__name__)
sockets = Sockets(app)

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

@app.route('/get')
def get():
   r.set('foo', 'bar')
   return r.get('foo')

@app.route('/set')
def set():
   s = redis.StrictRedis(host='10.9.21.212', port=5398, db=0, password='9145ef3c-9d30-43aa-b804-3aa66b79bf59')
   i = 0 
   while True:  
             i += 1  
             s.publish("first channel", "the i is " + str(i))  
             return ("the i is " + str(i))  
             time.sleep(1)  
   r = redis.StrictRedis(host='10.9.21.212', port=5398, db=0, password='9145ef3c-9d30-43aa-b804-3aa66b79bf59')
   p = r.pubsub() 
   p.subscribe("first channel")
   while True:  
            message = p.listen()  
            if message:  
                 return message  