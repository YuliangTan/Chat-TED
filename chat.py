import os
from flask import Flask
from flask import Response
from flask import request
from flask import abort

app = Flask(__name__)

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
    with open("login.log","wba") as fo:
        fo.write("\r\n")
        fo.write(request.args.get('info'))
        fo.write("\r\n")
    return request.args.get('info')
