import ssl
import socket
import argparse

PASS = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

parser = argparse.ArgumentParser()
parser.add_argument('hostname', type=str, action='store')
parser.add_argument('port', type=int, action='store', nargs='?', default=443)
args = parser.parse_args()

print '=' * 40
print 'Gaston : A SSL/TLS BEAST (CVE-20013389) Vulnerability Checker'
print '=' * 40 + '\n'
init 
print 'Target: %s:%d' % (args.hostname, args.port)
s = socket.socket()
s.connect((args.hostname, args.port))
ss = ssl.wrap_socket(s)
cipher, sslver, bitlen = ss.cipher()

if 'RC4' in cipher:
    msg  = PASS + 'NOT vulnerable to BEAST attack' + ENDC
    vuln = PASS + 'NO' + ENDC
else:
    msg  = FAIL + 'PRONE to BEAST attack.' + ENDC
    vuln = FAIL + 'YES' + ENDC

print '\n## %s ##\n' % msg
print 'Protocol: %s' % sslver
print 'Preferred Cipher: %s' % cipher
print 'Vulnerable: %s' % vuln
