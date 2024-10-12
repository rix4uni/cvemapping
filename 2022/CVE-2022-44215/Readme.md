# Introduction
A new vulnerability has been discovered affecting Titan FTP web server catalogued as CVE-2022-44215. Titan FTP is
a commertial software created by [South River Technologies](https://southrivertech.com/) that implements FTP protocol 
for file sharing. In its HTTP(S) version 19.X and prior, it has been proved to be vulnerable to an Open Redirection vulnerability. 


# Description
An Open redirection vulnerability consist into the server not correctly sanitizing the user’s input. Therefore, 
a redirection is done using the user-supplied input without sanitization (white/blacklisting). In this case, Titan FTP server 
performs a redirection when a backslash `\` is encountered in the URL. No matter if the backslash is in plaintext or URL encoded (%5C).
`https://<server>\<malicious_url>` will produce the server supplying a redirection to `\<malicious_url>`.


# Testing
To exploit this, the browser needs to understand the protocol of the location HTTP response header. This is to contain HTTP or HTTPS. 
To circumvent this, it is possible to supply instead of one backslash, two of them “\\”. This will be interpreted as a protocol separator
 and most browsers will use HTTP protocol by default. In the end, the working payload to achieve a redirection will be something similar 
 to this: `http[s]://<server>\\<malicious_url>`
 
![PoC](https://raw.githubusercontent.com/JBalanza/CVE-2022-44215/master/CVE_PoC.png)


To perform this test, also CURL can be used. However, bear in mind that CURL will detect it as bad crafted since “\” is prohibited by the 
standard RFC 2396. To bypass this using curl we can use the following command:

`Curl -i http[s]://<server> --request-target \\\\malicious.com`
 

# Proof of concept
Despite the issue, the exploitation is limited due to browsers normally rewrite starting backslashes “\” into “/”, producing that attacks 
using directly the plaintext will not work in most of the cases. Some workarounds could be done using HTML payloads that bypass browsers 
URL rewrite rules.

# Conclusion
According to Shodan, in December 2022 this server is publicly exposed at 1.278 servers worldwide:
 
![Shodan](https://raw.githubusercontent.com/JBalanza/CVE-2022-44215/master/shodan-TitanFTP.png)
 
This vulnerability could be used by attackers to perform social engineering attacks redirecting victims to fake FTP login pages or other 
phishing scenarios.

