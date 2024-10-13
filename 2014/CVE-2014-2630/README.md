# perf-exploiter (CVE-2014-2630) 

In one of our recent penetration tests we have abused a vulnerability affecting a suid binary called "`xglance-bin`". Part of *HP Performance Monitoring solution*, it allowed us to escalate our local unprivileged sessions on some Linux RHEL 7.x/8.x systems to `root`. To be very honest, it was not the first time we leveraged that specific vulnerability as we abused it frequently on many HP servers with RHEL installed since 2014.

There has been indeed a CVE registered for the flaw ([CVE-2014-2630](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-2630)) originally discovered by Tim Brown from Portcullis. However, up to today,there is no trace in the internet of a public exploit. Hence the idea to release our code. 

For more details please visit our [blog](https://www.redtimmy.com/).
