# CVE-2018-12596

Ektron CMS 9.20 SP2 allows remote attackers to call aspx pages via the "activateuser.aspx" page, even if a page
is located under the /WorkArea/ path, which is forbidden (normally available exclusively for local admins).

Exploit-DB publication at https://www.exploit-db.com/exploits/45577/ </br>
PacketStorm publication at https://packetstormsecurity.com/files/149734/Ektron-CMS-9.20-SP2-Improper-Access-Restrictions.html

# Timeline
================</br>
2018–06–08: Discovered </br>
2018–06–11: Retest staging environment </br>
2018–06–12: Restes live environment </br>
2018–06–19: Internal communication </br>
2018–06–21: Vendor notification </br>
2018–06–21: Vendor feedback </br>
2018–06–29: Vendor feedback product will be patched </br>
2018–06–29: Patch available </br>
2018–06–29: Agrements with the vendor to publish the CVE/Advisory </br>
2018–07–30: Internal communication </br>
2018–09–15: Patches tested on LAB environment <br>
2018–10–08: Public report <br>

# Episerver (Ektron Product 9.20 SP2) Patch and credits: 
https://support.episerver.com/hc/en-us/articles/115002828112-9-2-SP2-Site-Update

![vendor_patch_29 jun 18](https://user-images.githubusercontent.com/3140111/46631189-fd24d980-cb46-11e8-92ad-62ff33d016eb.png)

# Author
Alex Hernandez aka <em><a href="https://twitter.com/_alt3kx_" rel="nofollow">(@\_alt3kx\_)</a></em><br>
My current exploit list @exploit-db: https://www.exploit-db.com/author/?a=1074 <br>
CVE-2018-12596 with sexy screens here: https://medium.com/@alt3kx
