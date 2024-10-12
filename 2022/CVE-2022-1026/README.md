# kyocera-cve-2022-1026
An unauthenticated data extraction vulnerability in Kyocera printers, which allows for recovery of cleartext address book and domain joined passwords.


## Vulnerability Overview
Back in 2021 while on a pen test, I was tinkering with Kyocera's thick client application used to remotely administer printers. While proxying traffic from the application, I discovered that Kyocera's SOAP API on port 9091/TCP did not properly handle authentication when performing sensitive actions. Kyocera MFPs can be configured to with bind credentials for company domains, FTP credentials, fileshare credentials, etc. Unauthenticated, it is possible to retrieve all credentials stored by the MFP, in cleartext.

My full writeup can be found on Rapid7's blog: https://www.rapid7.com/blog/post/2022/03/29/cve-2022-1026-kyocera-net-view-address-book-exposure/

## Exploit overview
I do not believe this is currently fixed in all models and remains a 0-day, despite reports to the vendor. I was only able to test on a couple of models identified over the years, but whenever I find a Kyocera printer, this still works.

The python script connects to the MFP on TCP port 9091 and issues a SOAP request to create a new address book export. The printer responds with the address book object number, and then the script sleeps for a few seconds while the book is finished being created. Finally, the book is retrieved via another SOAP request. Within the book you'll find all configured credentials in cleartext. 

Feel free to submit a PR with improved parsing, as I never came back around to beautifying the output or exploit process.

### Usage:
`python3 getKyoceraCreds.py <printerip>`




