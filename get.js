var http = require('http');  
var server = http.createServer();  
server.on('request',function (req, res){  
      res.writeHead(200, {'Content-Type': 'text/plain'});  
      var name = require('url').parse(req.url,true).query.name  
      res.end('Hello World ' + name);  
    });  
    server.listen(process.env.VCAP_APP_PORT || 3000, null);  
    //console.log('Server running at http://127.0.0.1:1337/');  