# V0LTpwn
V0LTpwn (CVE-2019-11157) is a software-controlled fault attack on x86 processors. It is the first attack corrupting the integrity
of SGX enclaves.

## Description

All recent Intel processors exhibit a software interface for controlling core voltages without rebooting the system.
This feature is not required for normal operation but is used by expert users for performance optimizations. For instance, it is utilized by Intel's XTU application in the overclocking community. 

In V0LTpwn, we show that malicious software can use this interface to reduce the processor voltage to a critical threshold
at which certain instructions no longer operate correctly. This means that an attacker is able to induce bit flips 
in computations which are implemented with these instructions. We show in our paper how an attacker can manipulate cryptographic computations and even deviate the control flow of programs.

As the attack is controlled by software, the attacker does not require physical access to the machine. However, the attacker needs operating system privileges to utilize the voltage interfaces. It means that the vulnerability is not directly a threat for normal users. The main target are trusted execution environments like Intel's SGX. 

SGX is a security feature enabling applications to deploy enclaves which are protected even from the operating system. For instance, SGX can be used to run an application (securely) in an untrusted cloud environment. Previous attacks like Foreshadow have shown that secrets can be stolen from SGX enclaves over side channels. V0LTpwn is the first attack demonstrating how computations in SGX enclaves can be manipulated.    

We informed Intel in a responsible disclosure process about the vulnerability. Intel cooperated with us and started delivering patches to the affected platforms. For further details, we refer to official information in Intel's Security Advisory.  

## Paper
We provide all details about V0LTpwn in our research paper:

https://arxiv.org/abs/1912.04870

## Code

We will release our tool suite for further research soon.

## Further Information
Official information by Intel can be found at the following webpages: 

https://www.intel.com/content/www/us/en/security-center/advisory/intel-sa-00289.html

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-11157
