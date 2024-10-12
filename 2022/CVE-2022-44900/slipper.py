# Python 3 server example
from http.server import SimpleHTTPRequestHandler, BaseHTTPRequestHandler, HTTPServer
import time
import cgi
import py7zr
import base64

hostName = "localhost"
serverPort = 9999

class enum:
    FAVICON = """	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
	"""
	
    _BASE = """
    <!DOCTYPE html>
		<html lang="en">
		    <head>
			<title>Slipper</title>
			<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" />
		    </head>
		    
		    <body>
			<!-- Responsive navbar-->
			<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
			    <div class="container">
				<a class="navbar-brand" href="/">Slipper</a>     
			    </div>
			</nav>
			<!-- Page content-->
			<div class="container">
			    <div class="text-center mt-5">
			    
			       <div class="jumbotron" style="background-color:#e9ecef; padding: 50px;">
			       
					{content}
				
			       </div>
			    </div>
			</div>
		    </body>
		</html>
		"""
	
    GETPAGE = _BASE.format(content = """<p class="lead">Extract your 7z archives here</p>
				  <form action="extract" enctype="multipart/form-data" method="post">
				  <input id="file" accept=".7z" class="form-control" name="file" type="file" /><br><br>
				  <button class="btn btn-success" name="submit" type="submit"> Upload </button>
				  </form>""")
        
    POSTPAGE = _BASE.format(content = """<p> Files extracted from {}:
        {}</p>""")
        
    ERRPAGE = _BASE.format(content = """<div class="alert alert-danger" role="alert">
                                        An unexpected error occurred!
                                        </div>""")
    
    ERR404 = _BASE.format(content = """<div class="alert alert-danger" role="alert">
                                        Error 404, file not found!
                                        </div>""")

class handle(SimpleHTTPRequestHandler):   
    def _extract_archive(self, filename):
        archive = py7zr.SevenZipFile(filename, 'r')
        archive.extractall()
        return(archive.getnames())
        
    def send_error(self, code, message=None):
        if code == 404:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
	    
            self.wfile.write(bytes(enum.ERR404, "utf-8"))
        else:
            self.send_response(418)
            self.send_header("Content-type", "text/html")
            self.end_headers()
	    
            self.wfile.write(bytes(enum.ERRPAGE, "utf-8"))
 
    def do_GET(self):
        # It is not possible to use wfile.write to output the html page
        # as the default server behaviour is to either serve an index file or 
        # to show the directory listing.
        #
        # To prevent the server from showing the directory listing at the bottom of the
        # wfile.write content, we override the list_directory function.
        self.list_directory = lambda _:None 
        
        try:
            if self.path == '/favicon.ico':
                self.send_response(200)
                self.send_header("Content-type", "image/x-icon")
                self.end_headers()
		    
                self.wfile.write(bytes(base64.b64decode(enum.FAVICON)))
		        
            if self.path == '/':
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
		    
                self.wfile.write(bytes(enum.GETPAGE, "utf-8"))

            return SimpleHTTPRequestHandler.do_GET(self)
		
	    # If any exception is risen, returns a generic error page
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
	    
            self.wfile.write(bytes(enum.ERRPAGE, "utf-8"))
       
    def do_POST(self):
        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
                         })
                         
            filename = form['file'].filename
            data = form['file'].file.read()
            
            fileloc = filename
            fp = open(fileloc, 'wb')
            fp.write(data)
            fp.close()
            
            filelist = self._extract_archive(fileloc)
            
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            div = "<br>"
            
            self.wfile.write(bytes(enum.POSTPAGE.format(fileloc, div + div.join(["<a href={x}>{x}</a>".format(x=x) for x in filelist])), "utf-8"))
            
	    # If any exception is risen, returns a generic error page
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
	    
            self.wfile.write(bytes(enum.ERRPAGE, "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), handle)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
