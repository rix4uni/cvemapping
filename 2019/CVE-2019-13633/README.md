# CVE-2019-13633
**[Suggested description]**: Blinger.io v.1.0.2519 is vulnerable to Blind/Persistent XSS.  
**[Additional Information]**:  Blinger.io - is a platform which used by global clients such as FxPro, Alfa Bank, OneTwoTrip, Ivi, KupiVIP Group, Belavia, Wargaming, Yandex,
OZON, TCS Group Holding and others. Performing this attack allow criminals gather critical information about clients of targeted companies, and become basic point of many others attack vectors. An attacker can send arbitrary JavaScript code via a built-in communication channels, such as Telegram, WhatsApp, Viber, Skype, Facebook, and so on.   Code is executed within follow panels:  
- conversations/all  
- conversations/inbox  
- conversations/unassigned  
- conversations/closed

**[Vulnerability Type]**: Cross Site Scripting (XSS)  
**[Vendor of Product]**:  https://blinger.io/  
A letter was sent to the vendor about the vulnerability. Vulnerability was confirmed by vendor.  
**[Affected Component]**:  
https://app.blinger.io/conversations/all  
https://app.blinger.io/conversations/inbox    
https://app.blinger.io/conversations/unassigned    
https://app.blinger.io/conversations/closed      
**[Affected Product Code Base]**: Blinger Omnichannel helpdesk for customer support & sales - v.1.0.2519     
**[Attack Type]**: Remote    
**[Impact Denial of Service]**: False  
**[Impact Information Disclosure]**: True  
**[Attack Vectors]**:  
Attacker send malicious JavaScript code via communication channels built-in the customer web page. Transmitted JavaScript code will be executed in the administration panel of Help Desk service, allowing attacker to steal session cookie, perform phishing attack, gathering critical information about customer clients, etc.  
**[Discovered]**: Alexander Semenenko, Luka Safonov.  
**[Reference]**  
https://blinger.io/  
https://help.blinger.io/changelog  
**[Proof of Concept]**:    
Execution of malicious code and reflection in https://xsshunter.com/:
![stack Overflow]( https://github.com/Aleksander-Semenenko/CVE-2019-13633/blob/main/POC_CVE-2019-13633_3.png)

