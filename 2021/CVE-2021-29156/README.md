# CVE-2021-29156 Proof-of-Concept
(c) 2021 [GuidePoint Security](https://www.guidepointsecurity.com/)
Charlton Trezevant [charlton.trezevant@guidepointsecurity.com](mailto:charlton.trezevant@guidepointsecurity.com)

## Background

Today GuidePoint is pleased to [release](https://github.com/guidepointsecurity/CVE-2021-29156) a functional Proof-of-Concept tool for [CVE-2021-29156](https://nvd.nist.gov/vuln/detail/CVE-2021-29156), an LDAP injection vulnerability in ForgeRock OpenAM [v13.0.0](https://github.com/OpenIdentityPlatform/OpenAM/releases/tag/13.0.0). This vulnerability allows an attacker to extract a variety of information (such as a user’s password hash) from vulnerable OpenAM servers using a character-by-character brute force attack.

## Usage

To use this tool, simply adjust the `baseURL`, `proxy`, and `user` variables and run the script.

By default, this tool is configured to extract the password hash of the `amAdmin` user. As valid characters are discovered, the password hash string will be displayed in the console. Further adjustments may be made to the LDAP injection payloads if exfiltration of other data from the OpenAM instance is desired. 

## Additional Resources

For a more in-depth look at this vulnerability, PortSwigger has an [excellent writeup](https://portswigger.net/research/hidden-oauth-attack-vectors) of the exploit itself and its theory of operation.

