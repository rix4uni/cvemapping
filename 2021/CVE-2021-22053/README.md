# CVE-2021-22053
 CVE-2021-22053: Spring Cloud Netflix Hystrix Dashboard template resolution vulnerability
 
 ### Description
Applications using both `spring-cloud-netflix-hystrix-dashboard` and `spring-boot-starter-thymeleaf` expose a way to execute code submitted within the request URI path during the resolution of view templates. When a request is made at `/hystrix/monitor;[user-provided data]`, the path elements following `hystrix/monitor` are being evaluated as SpringEL expressions, which can lead to code execution.

### Affected VMware Products and Versions
Severity is high unless otherwise noted.
- Spring Cloud Netflix
  - 2.2.0.RELEASE to 2.2.9.RELEASE
  - Older, unsupported versions are also affected

### Mitigation
Users of affected versions should apply the following mitigation: Users should upgrade to 2.2.10.RELEASE+. No other steps are necessary. Releases that have fixed this issue include:
- Spring Cloud Netflix
  - 2.2.10.RELEASE+

### Credit
This vulnerability was identified and responsibly reported by threedr3am of SecCoder Security Lab (threedr3am@foxmail.com).

### References
https://www.first.org/cvss/calculator/3.0#CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L


#### Follow us 
#### [Vulnmachines](https://www.twitter.com/vulnmachines)
#### [YouTube](https://www.youtube.com/c/vulnmachines)
#### [Twitter](https://www.twitter.com/vulnmachines)
#### [Facebook](https://www.facebook.com/vulnmachines)
#### [LinkedIn](https://www.linkedin.com/company/vulnmachines)
