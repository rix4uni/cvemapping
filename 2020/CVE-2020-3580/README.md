<h1 align="center">
  <br>
 CVE-2020-3580 Automated Scanner 
</h1>

<h4 align="center">CVE-2020-3580 - Cisco Adaptive Security Appliance (ASA) Software and Cisco Firepower Threat Defense (FTD) Software XSS.</h4>


<p align="center">
<a href="https://nvd.nist.gov/vuln/detail/CVE-2020-3580"><img src="https://nvd.nist.gov/site-media/images/favicons/favicon-32x32.png"></a>
</p>
      


---





### Usage

```sh
▶ git clone "https://github.com/adarshvs/CVE-2020-3580.git"
▶ cd CVE-2020-3580
```
place domains/IP that you need to scan as .txt file format in the same folder
```sh
▶ python main.py
```

* Scan results will be stored under **output** folder
* Domains that were either not accessible or ingored during the scan will be listed under **output** folder as **ignored.txt** 
>Do not add https:// before domains lists
