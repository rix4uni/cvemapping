# CVE-2018-12018
Mitre https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-12018

The GetBlockHeadersMsg handler in the LES protocol implementation in Go Ethereum (aka geth) before 1.8.11 may lead to an access violation because of an integer signedness error for the array index, which allows attackers to launch a Denial of Service attack by sending a packet with a -1 query.Skip value. The vulnerable remote node would be crashed by such an attack immediately, aka the EPoD (Ethereum Packet of Death) issue.

**Mainnet**
```shell
python3 exploit.py --mainnet --enode 'enode'
```

**Testnet**
```shell
python3 exploit.py --enode 'enode'
```

You will may face dependecy issue with `py-evm` library. It is working with release [Trinity v0.1.0-alpha.16 "Ada Lovelace"](https://github.com/ethereum/py-evm/releases/tag/trinity-v0.1.0-alpha.16).
