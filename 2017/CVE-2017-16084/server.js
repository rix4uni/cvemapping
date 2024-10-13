#! /usr/bin/env node

var http = require('http');
var fs = require("fs");
var pathHelpers = require('path');
var beeline = require('beeline');
var packageJson = require('./package');
var program = require('commander');
var querystring = require('querystring');
var urlHelpers = require('url');


program
  .version(packageJson.version)
  .option('-p, --port [port]', 'Run on a custom port')
  .parse(process.argv);

function serverError(response, error){
    console.log(error);
    response.statusCode = 500;
    response.end();
}

function serveDir(request, response, path){
    fs.readdir(path, function(error, files){
        if(error){
            serverError(response, error);
            return;
        }

        var currentPath = urlHelpers.parse(request.url).pathname;

        response.writeHead(200, {"Content-Type": "text/html"});
        response.end(
            '<a href="../">../</a><br>' +
            files.map(function(fileName){
            return '<a href="' + currentPath + (currentPath === '/' ? '' : '/') + fileName + '?view">' + fileName + '</a>';
        }).join('<br>'));
    });
}

var mimeTypes = {
    'avi': 'video/x-msvideo',
    'mpg': 'video/mpeg',
    'mpeg': 'video/mpeg',
    'mp4': 'video/mp4'
}

function serveFile(request, response, path, info){
    var urlBits = request.url.split('?');

    if('view' in querystring.parse(urlBits[1])){
        response.writeHead(200, {"Content-Type": "text/html"});
        response.end(
            '<style>html, body{margin:0;background:black;}video{height:100%;width:100%}</style>' +
            '<video src="' + urlBits[0] + '" autoplay controls></video>'
        );
        return;
    }

    var total = info.size,
        contentType = mimeTypes[urlBits[0].split('.').pop()];

    // https://gist.github.com/paolorossi/1993068

    if (request.headers['range']) {
        var range = request.headers.range;
        var parts = range.replace(/bytes=/, "").split("-");
        var partialstart = parts[0];
        var partialend = parts[1];

        var start = parseInt(partialstart, 10);
        var end = partialend ? parseInt(partialend, 10) : total-1;
        var chunksize = (end-start)+1;

        var file = fs.createReadStream(path, {start: start, end: end});
        response.writeHead(206, { 'Content-Range': 'bytes ' + start + '-' + end + '/' + total, 'Accept-Ranges': 'bytes', 'Content-Length': chunksize, 'Content-Type': contentType });
        file.pipe(response);
    } else {
        response.writeHead(200, { 'Content-Length': total, 'Content-Type': contentType });
        fs.createReadStream(path).pipe(response);
    }
}

var router = beeline.route({
    '/`path...`': function(request, response, details){
        var path = process.cwd() + '/' + details.path;
        fs.stat(path, function(error, info){
            if(error){
                serverError(response, error);
                return;
            }

            if(info.isDirectory()){
                serveDir(request, response, path);
            }else{
                serveFile(request, response, path, info);
            }
        });
    }
});

var server = http.createServer(router);

var port = program.port || process.env.PORT || 8080;

server.listen(port);

console.log('serving ' + __dirname + ' on ' + port);