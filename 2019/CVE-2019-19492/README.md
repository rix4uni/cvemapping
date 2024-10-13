# FreeSWITCH Exploit (CVE-2019-19492)

This is an exploit script for FreeSWITCH vulnerabilities by Chocapikk and TrHacknon.

## Description

This script allows you to exploit FreeSWITCH vulnerabilities by executing remote commands. It supports exploitation of a single specified target or a list of targets specified in a file. It also has the ability to automatically generate a list of targets from Shodan.

## Prerequisites

- Python 3.6+
- `shodan` library (installed with `pip install shodan`)
- `rich` library (installed with `pip install rich`)
- `prompt_toolkit` library (installed with `pip install prompt_toolkit`)

## Usage

```
python exploit.py [--target TARGET --port PORT] [--list LIST] [--auto --pages PAGES] [--output FILE]
```

Options:
- `--target TARGET`: Specifies a single target IP to exploit.
- `--list LIST`: Specifies a file with a list of targets in the format ip:port. If port is not specified, default port will be used.
- `--port PORT`: Specifies a port for the target (default: 8021).
- `--auto`: Automatically generates a list of targets from Shodan.
- `--pages PAGES`: Specifies the number of pages for Shodan search (default: 1).
- `--output FILE`: Specifies the output file for storing the vulnerable targets.

If you use the `--target TARGET` or `--list LIST` option, the script will attempt to exploit the specified target(s).

If you use the `--auto` option, the script will automatically generate a list of targets from Shodan and attempt to exploit each target.

## Notes

- Make sure you have set your Shodan API key as the `SHODAN_API_KEY` environment variable.
- This tool is meant for educational purposes only. Misuse of this tool is strictly prohibited.

## Dorks

- Zoomeye: `service:"freeswitch-event"`
- Shodan: `product:"FreeSWITCH mod_event_socket` or `port:8021 Content-Type: auth/request`

## Warning

This script is provided for educational and ethical testing purposes only. Using this script for malicious activities is strictly prohibited. The authors, Chocapikk and TrHacknon, are not responsible for any misuse or illegal activities.

## Authors

- Chocapikk
- TrHacknon
