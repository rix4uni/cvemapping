# uboatdemo
### A demo server for CVE-2016-3955 (UBOAT)
Performs Linux heap buffer overflow, when USB/IP client begins sending control URBs.

## Building
The server is a standard simple Go program. You can build it the usual way assuming you have Go setup and configured according to [official instructions](https://golang.org/doc/install) with:
```
go get github.com/pqsec/uboatdemo/cmd/uboatsrv
```
The compiled binary should be in the `bin` directory of your configured `$GOPATH`.

## Additional information
https://pqsec.org/uboat-CVE-2016-3955/
