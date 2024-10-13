#  CVE-2021-21193

 - **Introduction to Hacking**

 - **Vulnerability case study presentations**

 - **March 2022**

 - ***Mehrzad Khodashenas, Setareh Sheikholeslamzadeh***



## Introduction

#### Quick Info
**CVE Dictionary Entry:**  
[CVE-2021-21193](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-21193)  
**NVD Published Date:**  
03/16/2021  
**NVD Last Modified:**  
12/03/2021  
**Source:**  
Chrome


|attribute| value|
|--|--|
| Severity | 7 |
| CVSS |(AV:N/AC:M/Au:N/C:P/I:P/A:P)  |
|Published  |03/05/2021  |
| Created |03/06/2021  |
|Added  | 03/05/2021 |
| Modified | 04/09/2021 |

[source](https://www.rapid7.com/db/vulnerabilities/google-chrome-cve-2021-21188/)


### Current Description

Use after free in Blink in Google Chrome prior to 89.0.4389.90 allowed a remote attacker to potentially exploit heap corruption via a crafted HTML page.

## what is CVE?
![enter image description here](https://cdn-clocb.nitrocdn.com/KWAwSZGWkokgJsWPPQsnurleOrkdYgfA/assets/static/optimized/rev-652f8a7/wp-content/uploads/2021/03/hacking-how-pressable-handles-it.jpg)

CVE, short for Common Vulnerabilities and Exposures, is a list of publicly disclosed computer security flaws. When someone refers to a CVE, they mean a security flaw that's been assigned a CVE ID number. Security advisories issued by vendors and researchers almost always mention at least one CVE ID. CVEs help IT professionals coordinate their efforts to prioritise and address these vulnerabilities to make computer systems more secure.
[source](https://www.redhat.com/en/topics/security/what-is-cve)

## Google chrome vulnerability
![enter image description here](https://thehackernews.com/images/-FOgCdN3CSOk/YUAgGS1bB1I/AAAAAAAADyc/2oKkq_Mon1AnpsrRVosSNgmXm6ZdbQTXACLcBGAsYHQ/s728-e1000/chrome-update.jpg)

The chrome team have published an announcement on march 2021 that If you use Google Chrome on any of your devices, it is urgent that you update it immediately. There are frequent Google Chrome updates, but the most recent patch, stable build 89.0.4389.90, patches several vulnerabilities, three of which have a high severity rating, and one of which has already been exploited by cybercriminals and hackers.
[source](https://preemo.com/cve-2021-21193-vulnerability) 
It was one of the high severity rating vulnerabilities called CVE-2021-21193. It is a vulnerability in Google Chrome’s browser engine Blink, the main component responsible for converting HTML code into the well-designed Web pages you’re used to browsing. This problem impacts certain unidentified processing in the Blink component and the manipulation with an unknown input leads to a memory corruption vulnerability. This vulnerability that has been exploited by malefactors suggests all users need to update to version 89.0.4389.90. It is a use-after-free vulnerability, which means Blink had trouble clearing memory.
[source](https://www.kaspersky.com/blog/google-chrome-cve-2021-21193/39013/)

### A little information about the attack

The weakness was disclosed 03/05/2021. No form of authentication is needed for a successful exploitation, but it demands that the victim is doing some kind of user interaction. There is also an estimated price for an exploit that is around USD $5k-$25k calculated on 03/28/2021. [https://vuldb.com/?id.170687](https://vuldb.com/?id.170687)


## Use after free
While this seems trivial and mundane, a use-after-free vulnerability’s most common consequences are data corruption and arbitrary code execution, which, according to the National Vulnerability Database’s description of the CVE-2021-21193 vulnerability itself can allow “a remote attacker to potentially exploit heap corruption via a crafted HTML page.”
[source](https://preemo.com/cve-2021-21193-vulnerability)

### What is a Use-After-Free and how does it occur?

Use-After-Free (UAF) is a vulnerability related to incorrect use of dynamic memory during program operation. If after freeing a memory location, a program does not clear the pointer to that memory, an attacker can use the error to hack the program.

UAF vulnerabilities stem from the mechanism of dynamic memory allocation. Unlike the stack, dynamic memory (also known as the heap) is designed to store large amounts of data. Programmers can allocate blocks of arbitrary size in it, which tasks within a program can then either modify or free and return to the heap for subsequent use by other tasks in the same program.

Programs must continually verify which areas of the heap are free and which are occupied since dynamic memory is reallocated often. Headers help by referencing allocated memory areas. The starting address of the appropriate block is contained in each header. UAF bugs arise when programs do not manage these headers properly.

### How do UAF bugs happen?
Pointers in a program refer to data sets in dynamic memory. If a data set is deleted or moved to another block but the pointer, instead of being cleared (set to null), continues to refer to the now-freed memory, the result is a dangling pointer. If the program then allocates this same chunk of memory to another object (for example, data entered by an attacker), the dangling pointer will now reference this new data set. In other words, UAF vulnerabilities allow for code substitution.

### Exploiting UAF
An attacker can use UAFs to pass arbitrary code, or a reference to it, to a program and navigate to the beginning of the code by using a dangling pointer. In this way, the cybercriminal can obtain control of the victim's system by executing malicious code.
[source](https://encyclopedia.kaspersky.com/glossary/use-after-free/)

An anonymous security researcher reported CVE-2021-211193 on March 9, and Google rushed out a fix in just three days. That rush might be attributable to the vulnerability’s real-world exploitation; crooks have already used the vulnerability, and that is reason enough for everybody to patch Google Chrome ASAP. 
[source](https://www.kaspersky.com/blog/google-chrome-cve-2021-21193/39013/)

##  The big takeaway from the CVE-2021-21193 vulnerability

Google usually doesn’t release information about vulnerabilities until after they have been patched, and the CVE-2021-21193 vulnerability was patched no more than three days after it was reported by an anonymous security researcher, which most likely means that the vulnerability had already been exploited in a real-world situation. A good rule of thumb is that if a giant tech company like Google is taking a security problem seriously, so should the rest of us.

But there’s another important takeaway here, which is that these tech giants, and their products, aren’t perfect; like the rest of us, they, too, are part of the constant race to keep systems and tools secure for end-users like you. It is absolutely vital to keep your software patched with the latest updates from their developers, as the most recent updates are the ones that have been crafted to minimise the threat of rapidly evolving and advancing cyber threats.
[source](https://preemo.com/cve-2021-21193-vulnerability)

#### Useful links:

[https://vuldb.com/?id.170687](https://vuldb.com/?id.170687)
