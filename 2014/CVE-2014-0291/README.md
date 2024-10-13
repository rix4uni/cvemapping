patch-openssl-CVE-2015-0291_CVE-2015-0204
===========================

Patch openssl with ansible 

# Usage :
    pip install ansible
    ansible-playbook -i your_inventory_file patch-openssl-CVE-2015-0291_CVE-2015-0204

your_inventory_file just need to contain your server list :
```
192.168.0.10
webserver1.example.com
webserver2.example.com
db1.example.com
```
# Support
- Upgrade openssl on RedHat Family OS
- Restart some services impacted

# Test if you need to patch
```
% openssl version -a
% rpm -q --changelog openssl | grep CVE-2015-0291
% rpm -q --changelog openssl | grep CVE-2015-0204
```
# More information
- CVE-2015-0291 & CVE-2015-0204
- https://www.openssl.org/news/secadv_20150319.txt

# Author Information
- Original : DAUPHANT Julien
- Modified by : Niko Stojanovski
