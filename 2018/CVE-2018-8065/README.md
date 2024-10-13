# Flexense HTTP Server <= 10.6.24 - Denial Of Service Vulnerability

        # Exploit Title: Flexense HTTP Server <= 10.6.24 - Denial Of Service Vulnerability
        # Date: 03-09-2018
        # Exploit Author: Ege Balcı
        # Vendor Homepage: http://www.syncbreeze.com
        # Software Link: https://github.com/EgeBalci/Sync_Breeze_Enterprise_10_6_24_-DOS/raw/master/syncbreezeent_setup_v10.6.24.exe
        # Version: 10.6.24
        # Tested on: Windows 7/10
        # CVE: 2018-8065


This module triggers a Denial of Service vulnerability in the Sync Flexense HTTP Server . After installing the software, web server should be enabled via Options->Server->Enable web server on port. Module triggers a user space write access violation on syncbrs.exe memory region. Number of requests that will crash the server changes between 200-1000 depending on the OS version and system memory. Sync Breeze Enterprise 10.6.24 version reportedly vulnerable.

# Exploits

[MSF Module](https://github.com/EgeBalci/Flexense_HTTP_Server_DOS/blob/master/flexense_http_server_dos.rb) <br>
[PYTHON](https://github.com/EgeBalci/Flexense_HTTP_Server_DOS/blob/master/dos.py)
