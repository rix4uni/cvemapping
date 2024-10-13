import argparse
import struct
import sys

from twisted.python import log
from twisted.internet import defer, protocol, reactor, ssl
from twisted.internet.endpoints import (
    TCP4ClientEndpoint, TCP4ServerEndpoint, connectProtocol)

class BufferedProtocol(protocol.Protocol, object):
    def __init__(self):
        self._buffer_enabled = True
        self._buffer = b''
        self._deferred = None
        self._wait_length = 0

        super(BufferedProtocol, self).__init__()

    def _read_buffer(self, length):
        assert len(self._buffer) >= length

        if length == 0:
            # return the entire buffer
            data, self._buffer = self._buffer, b''
            return data
        else:
            data, self._buffer = self._buffer[:length], self._buffer[length:]
            return data

    def stop_buffering(self):
        assert self._deferred is None

        self._buffer_enabled = False

        if len(self._buffer):
            self.rawDataReceived(self._buffer)
            self._buffer = b''

    def waitfor(self, length):
        assert isinstance(length, int)
        assert self._deferred is None

        if len(self._buffer) >= length:
            return defer.succeed(self._read_buffer(length))
        else:
            self._wait_length = length
            self._deferred = defer.Deferred()
            return self._deferred

    def connectionLost(self, reason):
        log.msg('{} connection lost: {}'.format(self.__class__, reason))
        if self._deferred:
            self._deferred.errback(reason)

    def dataReceived(self, data):
        log.msg('{} received: {!r}'.format(self.__class__, data))
        if not self._buffer_enabled:
            self.rawDataReceived(data)
        else:
            self._buffer += data
            if self._deferred and len(self._buffer) >= self._wait_length:
                data = self._read_buffer(self._wait_length)
                d = self._deferred
                self._deferred = None
                self._wait_length = 0

                d.callback(data)

    def rawDataReceived(self, data):
        raise NotImplementedError()

class MySQLForwardBaseProtocol(BufferedProtocol):
    SSL_FLAG = 0x00000800

    def __init__(self, peer=None):
        self.peer = peer

        super(MySQLForwardBaseProtocol, self).__init__()

    @staticmethod
    def parse_header(packet):
        assert len(packet) >= 4
        header = packet[:4]
        (length_s, seq_id) = struct.unpack('<3sB', header)
        (length,) = struct.unpack('<L', (length_s + b'\0'))
        return length, seq_id

    @staticmethod
    def make_header(length, seq_id):
        length_s = struct.pack('<L', length)[:3]
        return struct.pack('<3sB', length_s, seq_id)

    @staticmethod
    def modify_seq(packet, delta=1):
        assert len(packet) >= 4
        (seq,) = struct.unpack('<B', packet[3])
        seq = (seq + delta) & 0xFF
        packet = packet[:3] + struct.pack('<B', seq) + packet[4:]
        return packet

    @classmethod
    def make_ssl_request(cls, client_handshake):
        # SSL handshake request is the first 32 bytes of the client
        # handshake packet, so truncate. keep the seq_id, though
        # XXX seq_id is 1 here. always.
        _length, seq_id = cls.parse_header(client_handshake)
        client_ssl_handshake = client_handshake[4:36]

        # set the SSL flag
        # XXX client capabilities flags are first 4 bytes
        cap_flags_s = client_ssl_handshake[:4]
        (cap_flags,) = struct.unpack('<I', cap_flags_s)
        cap_flags |= cls.SSL_FLAG
        cap_flags_s = struct.pack('<I', cap_flags)
        client_ssl_handshake = cap_flags_s + client_ssl_handshake[4:]

        # then add header
        header = cls.make_header(len(client_ssl_handshake), seq_id)
        return header + client_ssl_handshake

    @classmethod
    def modify_server_handshake(cls, packet):
        header, handshake = packet[:4], packet[4:]

        # XXX assume handshake packet v10
        # Find the capabilities flags field:
        # 1 byte proto version
        # nul-terminated server version
        # 4 bytes connection id
        # 8 bytes auth data
        # 1 byte filler
        # 2 bytes capabilities flags <-- our target!
        # ...
        i = handshake.index(b'\0', 1)
        cap_flags_i = i+14
        cap_flags_s = handshake[cap_flags_i:cap_flags_i+2]
        (cap_flags,) = struct.unpack('<H', cap_flags_s)

        if not (cap_flags & cls.SSL_FLAG):
            raise Exception('why are we even doing this?')

        # unset the SSL flag
        cap_flags = cap_flags ^ cls.SSL_FLAG
        cap_flags_s = struct.pack('<H', cap_flags)
        handshake = (
            handshake[:cap_flags_i] + cap_flags_s + handshake[cap_flags_i+2:])

        return (header + handshake)

    def connectionLost(self, reason):
        super(MySQLForwardBaseProtocol, self).connectionLost(reason)
        if self.peer is not None:
            self.peer.transport.loseConnection()

    def rawDataReceived(self, data):
        self.peer.transport.write(data)

    @defer.inlineCallbacks
    def read_packet(self):
        # read header length
        header = yield self.waitfor(4)
        length, _seq_id = self.parse_header(header)

        # read payload
        payload = yield self.waitfor(length)

        defer.returnValue(header + payload)

class MySQLForwardServerProtocol(MySQLForwardBaseProtocol):
    @defer.inlineCallbacks
    def connectionMade(self):
        try:
            # we'll handle all the handshake logic here
            self.peer = yield connectProtocol(
                self.factory.dest, MySQLForwardClientProtocol(self))
            server_handshake = yield self.peer.read_packet()
            server_handshake = self.peer.modify_server_handshake(
                server_handshake)
            self.transport.write(server_handshake)

            # ok, now get the client handshake
            client_handshake = yield self.read_packet()

            # use the client handshake to generate an SSL request
            ssl_request = self.make_ssl_request(client_handshake)
            self.peer.transport.write(ssl_request)
            self.peer.transport.startTLS(ssl.ClientContextFactory())

            # then send the original client handshake packet. For this
            # and the next couple packets, the server and client will
            # have different ideas of what the packet sequence IDs
            # should be (we just sent an extra packet to the server
            # and the client doesn't know about it). So every client
            # -> server packet needs to have its seq_id incremented;
            # server -> client packets need to have them decremented
            client_handshake = self.modify_seq(client_handshake, 1)
            self.peer.transport.write(client_handshake)

            # send packets back and forth until the client resets
            # the sequence numbers
            yield self.forward_until_seq_reset()

            # start forwarding traffic with no further manipulation
            self.stop_buffering()
            self.peer.stop_buffering()

        except Exception:
            self.transport.loseConnection()
            log.err()

    @defer.inlineCallbacks
    def forward_until_seq_reset(self):
        # the first packet we forward is server-to-client
        increment = -1
        source, dest = self.peer, self

        while True:
            # read packet
            next_packet = yield source.read_packet()
            _length, seq = self.parse_header(next_packet)

            # increment or decrement sequence number if it was not reset
            if seq != 0:
                next_packet = self.modify_seq(next_packet, increment)
            dest.transport.write(next_packet)

            # if sequence number was reset, we're done
            if seq == 0:
                break

            # reverse direction!
            increment = -increment
            source, dest = dest, source

class MySQLForwardClientProtocol(MySQLForwardBaseProtocol):
    pass

class MySQLForwardServerFactory(protocol.Factory):
    protocol = MySQLForwardServerProtocol

    def __init__(self, dest_host, dest_port):
        self.dest = TCP4ClientEndpoint(reactor, dest_host, dest_port)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-p', '--listen-port', type=int, default=3306)
    p.add_argument('-i', '--listen-interface', default='127.0.0.1')
    p.add_argument('dest')
    args = p.parse_args()

    if ':' in args.dest:
        dest_host, dest_port = args.dest.split(':')
        dest_port = int(dest_port)
    else:
        dest_host = args.dest
        dest_port = 3306

    log.startLogging(sys.stdout)
    log.msg('listen: {}:{}; connect: {}:{}'.format(
            args.listen_interface, args.listen_port, dest_host, dest_port))

    endpoint = TCP4ServerEndpoint(
        reactor, args.listen_port, interface=args.listen_interface)
    endpoint.listen(MySQLForwardServerFactory(dest_host, dest_port))
    reactor.run()

if __name__ == '__main__':
    main()
