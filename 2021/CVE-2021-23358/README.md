# Detection-script-for-cve-2021-23358
Detection script for cve-2021-23358
I have created a Detection script for CVE-2021-23358 , which will detect the vulnerable version of node underscore be it installed as an open-source tool or just the libraries are being used.
This script has three features, It will detect the versions of underscore from
1)	Using the direct npm command 
2)	Version written in the PATH of the libraries 
3)	Inside the library itself 

The package underscore from 1.13.0-0 and before 1.13.0-2, from 1.3.2 and before 1.12.1 are vulnerable to Arbitrary Code Injection via the template function, particularly when a variable property is passed as an argument as it is not sanitized.
And the library’s underscore uses are 
1)	Node-underscore
2)	Libjs-underscore
3)	Underscore 


![image](https://user-images.githubusercontent.com/106553324/221375496-deb9ff2c-63a7-4b70-b8c8-5edd6824cc5e.png)



