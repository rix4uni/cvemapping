import requests
import json
import os
from setArgs import args
import pathlib
import time


hitList = []

class Scans:
    
    def __init__(self):
        self.fileScan = args.file
        self.port = args.port
        self.timeout = args.timeout
        self.singleIP = args.target
        self.save = args.save

        self.headers = {'Content-Type': 'application/json; charset=UTF-8',
                    'X-JNAP-Action':'http://cisco.com/jnap/core/GetDeviceInfo',
                    'X-JNAP-Authorization': 'null',
                    'X-Requested-With' : 'XMLHttpRequest'}

        self.passHeader = {'X-JNAP-ACTION':'http://cisco.com/jnap/core/IsAdminPasswordDefault'}

    def file_scan(self):
        print("Starting to scan file " + self.fileScan + '\n')
        time.sleep(2)
        self.filePath = os.getcwd()

        with open (self.filePath + '/' + '{}'.format(self.fileScan),'r') as f:
            for ip in f.read().splitlines():

                try:
                    req = requests.get("http://" + ip + ":" + str(self.port), headers=self.headers,timeout=int(self.timeout))
                except requests.RequestException:
                    print("A request error occured @ " + ip + '\n')
                    continue
                
                if req.status_code == 200:
                    print("200 returned at " + ip + '\n')
                    try:
                        deviceReq2 = requests.post("http://" + ip + ":" + str(self.port) + '/JNAP/',headers=self.headers,data="{}",timeout=int(self.timeout)).text
                    except requests.RequestException:

                        print("A requests error occured @ "+ ip + '\n')
                        continue

                    try:
                        deviceJson2 = json.loads(deviceReq2)
                    
                        if deviceJson2['output']['manufacturer']:
                            print("Linksys found!")
                            hitList.append(ip)

                    except json.decoder.JSONDecodeError:
                        print("Key Error @ " + ip)
                        continue
                    except KeyError:
                        print("Key Error @ " + ip)
                    except TypeError:
                        print("Type error @ " + ip)

                else:
                    print("Requests did not return 200")
                    continue
        
        f.close()
        

        

    def single_scan(self):

        try:
            req = requests.get("http://" + self.singleIP + ":" + str(self.port))
        
            if req.status_code == 200:
            
                deviceReq = requests.post("http://" + self.singleIP + ":" + str(self.port) + '/JNAP/', headers = self.headers, data="{}",
                timeout = int(self.timeout)).text
        except requests.RequestException:
            print("Request error at " + self.singleIP)
            

            try:
                deviceJson = json.loads(deviceReq)
                    
                if deviceJson['output']['manufacturer']:
                    print("Linksys found!" + '\n')
                    hitList.append(self.singleIP)
                else:
                    print(self.singleIP + "is not a linksys smart device")

            except Exception:
                print("Json error at " + self.singleIP)
            else:
                print("Linksys Device Not Found")
    
    def save_hits(self):
        numberHits = str(len(hitList))
        

        if len(hitList) == 0 :
            print("There are no addresses to save")
        else:
            listLength = len(hitList)
            print("There are " + str(listLength) + " addresses in the list to save")
            getPath = os.getcwd()
            savePath = getPath + "/"
            file = pathlib.Path(self.save)

            if file.exists():
                print("File found, appending results to existing file.")
                with open(savePath + self.save,'a') as savehits:
                    for ip in hitList:
                        savehits.write(ip + '\n')
                savehits.close()
            else:
                print("File not found. creating it now and writing results")
                with open(savePath + self.save, 'w+') as savehits:
                    for ip in hitList:
                        savehits.write(ip + '\n')
                    print('\n')
                    print("File created and written to")
                savehits.close()

class Leaks:
    passwordsFound = []
    def __init__(self,dftpassHeader):
        self.default_passCheck = args.checkPass
        self.getpassHeader = dftpassHeader
        self.fileArg = args.file
        self.target = args.target
        self.timeout = args.timeout

    def check_pass(self):
        print("Starting check for default passwords" + '\n')
        

        if self.fileArg:
            if self.default_passCheck:
                for ip in hitList:
                    try:
                        createdHeader = {'X-JNAP-ACTION' : '{}'.format(self.getpassHeader)}
                        req = requests.post("http://" + ip + "/JNAP/",headers=createdHeader,data='{}',timeout=int(self.timeout)).text
                        passJson = json.loads(req)
                        passResult = passJson['output']['isAdminPasswordDefault']
                    
        # once we get the rersults check if they are true or false then print result
                        if passResult == True:
                            print('Default Password IN uSe @ ' + ip)
                        elif passResult == False:
                            print("No Default Creds Found Yet")

                    except requests.exceptions.ConnectionError:
                        print("Something happend when getting the creds from " + ip)
                        continue

        elif self.target and self.default_passCheck:
            try:
                createdHeader = {'X-JNAP-ACTION' : '{}'.format(self.getpassHeader)}
                req = requests.post("http://" + self.target + "/JNAP/",headers=createdHeader,data='{}',timeout=int(self.timeout)).text
                passJson = json.loads(req)
                passResult = passJson['output']['isAdminPasswordDefault']
                    
        # once we get the rersults check if they are true or false then print result
                if passResult == True:
                    print('Default Password IN uSe @ ' + ip)
                elif passResult == False:
                    print("No Default Creds in use")
                
            except requests.exceptions.ConnectionError:
                print("Something happend when getting the creds from " + ip)
        

        else:
            print("something happened while searching for creds")

        print('\n')

        



