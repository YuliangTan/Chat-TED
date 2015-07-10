import os
from flask import Flask
from flask import Response

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

@app.route('/post', methods=['GET'])
def post():
    posts = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    try:
        id = int(request.args.get('id', 0)) 
    except ValueError:
        abort(404)     
    else:
        if id in posts:
            return 'post_id = {0}'.format(id)
        else:
            abort(404)
