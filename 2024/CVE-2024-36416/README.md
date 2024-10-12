# CVE-2024-36416
Tool for validating CVE-2024-36416

## Usage
```
pip3 install -r requirements.txt
python3 sukuna.py --help
python3 sukuna.py --url http://<target>.<tld>/<crm-root> --validate --payload-test
```
<div align="center"">
  
  ![detection-tool2](https://github.com/kva55/CVE-2024-36416/assets/60018788/0dcae9fc-bd45-45ee-b49c-9818f678d27a)

</div>

## Server-Side Log File Check
Verify the server-side file, if the log file ``\service\example\proxy.log`` is >=25MB, the server is likely vulnerable.

<div align="center"">

  ![server-side](https://github.com/kva55/CVE-2024-36416/assets/60018788/b0414c0d-3f76-441e-bfa1-3f632afcadb5)

</div>

## Issues
- Downloading the zipped folder may cause windows defender to yell "Trojan:Script/Wacatac"
- Supply the crm root page (could be '/suite7/docroot/', '/SuiteCRM-7.14.3/', or '/'), if you supply the full path the detection may work but the code isn't programmed to step back through your supplied path
- This exploit is mostly stateless, so while the reported files could respond with a 403/404 the best way to verify is to do a limited upload with the ``--payload-test`` arg 
