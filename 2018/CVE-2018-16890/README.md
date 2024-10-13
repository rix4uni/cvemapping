# CVE-2018-16890

An out-of-bounds read flaw was found in the way curl handled NTLMv2 type-2 headers. When connecting to a remote malicious server which uses NTLM authentication, the flaw could cause curl to crash.

A simple script to check your curl.
