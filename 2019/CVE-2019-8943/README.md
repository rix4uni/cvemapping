# WordPress Crop-Image CVE-2019-8943

A python3 script for WordPress Crop-Image CVE-2019-8943 Authenticated Remote Code Execution (RCE). It drops a malicious PHP backdoor.

## Getting Started

### Executing program

* RCE
```
python3 wp_rce.py -t http://wordpress.rce/ -u admin -p password -m twentytwenty
```

## Help

For help menu:
```
python3 wp_rce.py -h
```

## Disclaimer
All the code provided on this repository is for educational/research purposes only. Any actions and/or activities related to the material contained within this repository is solely your responsibility. The misuse of the code in this repository can result in criminal charges brought against the persons in question. Author will not be held responsible in the event any criminal charges be brought against any individuals misusing the code in this repository to break the law.