# Decrypt FortiManager configuration secrets (CVE-2020-9289)

CVE-2020-9289 and CVE-2019-6693 are related to the same default and hardcoded key.

The only differences on the decryption routine implemented in FortiManager/FortiAnalyzer are:

- The IV handling (all the 16 bytes are provided before the encrypted data from digits).
- The last encrypted block is stripped from the output so it needs junk to be appended then removed from the cleartext.

See https://www.fortiguard.com/psirt/FG-IR-19-007 for more details.

