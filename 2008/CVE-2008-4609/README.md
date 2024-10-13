# sockstress
Sockstress (CVE-2008-4609)  implementation using Go

## Install
```
go get github.com/marcelki/sockstress
```

## Usage
```
Usage: sockstress [options...] <ip-address>

Options:
  -p    The destination port to attack.
  -i    The network interface to use.
  -d    The delay between SYN packets
        You can choose your unit of time (e.g. 1ns, 0.001s)
  -h    Display this help.
```
