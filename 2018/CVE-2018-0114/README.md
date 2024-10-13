# POC-CVE-2018-0114
This repository contains the POC of an exploit for node-jose &lt; 0.11.0

## Getting Started

A vulnerability in the Cisco node-jose open source library before 0.11.0 could allow an unauthenticated, remote attacker to re-sign tokens using a key that is embedded within the token. The vulnerability is due to node-jose following the JSON Web Signature (JWS) standard for JSON Web Tokens (JWTs). This standard specifies that a JSON Web Key (JWK) representing a public key can be embedded within the header of a JWS. This public key is then trusted for verification. An attacker could exploit this by forging valid JWS objects by removing the original signature, adding a new public key to the header, and then signing the object using the (attacker-owned) private key associated with the public key embedded in that JWS header. (https://nvd.nist.gov/vuln/detail/CVE-2018-0114).

:warning: For PTL students  :warning:&nbsp;
```diff
-If you are a student of PentesterLAB, I highly recommend you to try to create the code yourself to exploit this vulnerability!
```

### Prerequisites

```
python 3 -> (Stating from the last merge)
```
```
python lib: base64,urllib,rsa,sys
```

## Running the tests

To run the script just run the following command:

```
python jwk-node-jose.py "payload" {key-size}
```
(key-size whitout {} )


## Authors

* **Andrea Cappa** - *Initial work* - [GitHub](https://github.com/zi0Black) - [Twitter](https://twitter.com/zi0Black)
* **Louis Nyffenegger** - *support and help* - [Louis](https://pentesterlab.com) - [Referal ;)](https://pentesterlab.com/referral/RxYT1QSCQcnD1g)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
- @eshaan7 - 2019
- @LighTend3r - 2023
