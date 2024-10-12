# CVE-2023-47014-Sticky-Notes-App-Using-PHP-with-Source-Code-v1.0-CSRF-to-CORS

Exploit Author: emirhanerdogu

# Vendor Homepage

https://www.sourcecodester.com/php/16928/sticky-notes-app-using-php-source-code.html

# Software Link

https://www.sourcecodester.com/download-code?nid=16928&title=Sticky+Notes+App+Using+PHP+with+Source+Code

# Overview

Cross Site Request Forgery vulnerability in Remyandrade Sticky Notes
App Using PHP with Source Code v.1.0 allows a remote attacker to obtain sensitive information via a crafted payload to the add-note.php component.

# Vulnerability Details

CVE ID: CVE-2023-47014.  
Affected Version: Sticky-Notes V1.0  
Vulnerable File: Origin  
Parameter Names: -  
Attack Type: Local  

# Description

When the Origin header information is added in the annotation field, the CORS vulnerability does not occur. However, when the CSRF PoC was created and the Burp Collaborator address was added to it, the CORS vulnerability was triggered.

# Proof of Concept (PoC) :

Request and Response:

![image](https://github.com/emirhanerdogu/CVE-2023-47014-Sticky-Notes-App-Using-PHP-with-Source-Code-v1.0-CSRF-to-CORS/assets/32299032/4e7dfd72-6f00-4165-abe1-17f70482c51a)

CSRF PoC:

![image](https://github.com/emirhanerdogu/CVE-2023-47014-Sticky-Notes-App-Using-PHP-with-Source-Code-v1.0-CSRF-to-CORS/assets/32299032/cecd15b3-f7dc-4c97-8d41-f377440647db)

![image](https://github.com/emirhanerdogu/CVE-2023-47014-Sticky-Notes-App-Using-PHP-with-Source-Code-v1.0-CSRF-to-CORS/assets/32299032/f7fe9761-7f34-411b-9e19-9aad9f67563b)

Exploit:

![image](https://github.com/emirhanerdogu/CVE-2023-47014-Sticky-Notes-App-Using-PHP-with-Source-Code-v1.0-CSRF-to-CORS/assets/32299032/92ff35bc-6b3b-43a4-8014-d6dcc9752238)




