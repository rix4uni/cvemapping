# https-nj.gov---CVE-2018-14042
#### Vulnearability Report of the New Jersey official site
In Bootstrap prior to 4.1.2, XSS is possible in the main collapse data attribute.
The data-target attribute, the data-parent attribute and the data-container is vulnerable to Cross-Site Scripting attacks.

`<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"></script>`

`<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>`

`<button data-toggle="collapse" data-target="<img src=x onerror=alert(0)>">Test</button> `

# RECOMMENDATION
The fix for this specific issue could be changing getTargetFromTrigger function:

`return $(target)`
to:

`return $(document.querySelector(target))`
but it seems the same problem is present in other places too.

Here is another example:

`<a href="<img src=x onerror=alert(0)>" data-dismiss="alert">Test</a>`
# REFERENCES
http://packetstormsecurity.com/files/152787/dotCMS-5.1.1-Vulnerable-Dependencies.html	
http://packetstormsecurity.com/files/156743/OctoberCMS-Insecure-Dependencies.html	
http://seclists.org/fulldisclosure/2019/May/10	
http://seclists.org/fulldisclosure/2019/May/11	
http://seclists.org/fulldisclosure/2019/May/13	
https://access.redhat.com/errata/RHSA-2019:1456	
https://blog.getbootstrap.com/2018/07/12/bootstrap-4-1-2/	 
https://github.com/twbs/bootstrap/issues/26423	
https://github.com/twbs/bootstrap/issues/26627	
https://github.com/twbs/bootstrap/pull/26630	 
https://lists.apache.org/thread.html/519eb0fd45642dcecd9ff74cb3e71c20a4753f7d82e2f07864b5108f@%3Cdev.drill.apache.org%3E	
https://lists.apache.org/thread.html/52e0e6b5df827ee7f1e68f7cc3babe61af3b2160f5d74a85469b7b0e@%3Cdev.superset.apache.org%3E	
https://lists.apache.org/thread.html/b0656d359c7d40ec9f39c8cc61bca66802ef9a2a12ee199f5b0c1442@%3Cdev.drill.apache.org%3E	
https://lists.apache.org/thread.html/f9bc3e55f4e28d1dcd1a69aae6d53e609a758e34d2869b4d798e13cc@%3Cissues.drill.apache.org%3E	
https://lists.apache.org/thread.html/r3dc0cac8d856bca02bd6997355d7ff83027dcfc82f8646a29b89b714@%3Cissues.hbase.apache.org%3E	
https://seclists.org/bugtraq/2019/May/18	
https://www.oracle.com/security-alerts/cpuApr2021.html

