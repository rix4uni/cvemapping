#!/usr/bin/env python
from boofuzz import *
import sys


def hello(target, logger, session, *args, **kwargs):
    try:
        banner = target.recv(1000)
    except Exception:
        logger.log_info("Target down. Exiting.")
        sys.exit(-1)

    logger.log_check("Banner received")
    if not banner.startswith("220 Welcome to Easy File Sharing FTP Server!"):
        logger.log_fail("Incorrect banner: {}".format(banner))
        sys.exit(-2)


def main():
    session = Session(
            target=Target(connection=SocketConnection("192.168.0.101", 21, proto='tcp')),
            )

    s_initialize(name="Command")
    s_static("USER ftptest\r\n")
    s_static("PASS ")
    s_string("1")
    s_static("\r\n")

    session.connect(s_get("Command"), callback=hello)

    session.fuzz()


if __name__ == "__main__":
    main()
