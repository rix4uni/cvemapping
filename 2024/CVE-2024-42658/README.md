# CVE-2024-42658
 CVE-2024-42658 An issue in wishnet Nepstech Wifi Router NTPL-XPON1GFEVN v1.0 allows a remote attacker to obtain sensitive information via the cookies parameter

CVE-2024-42658:

Summary: A vulnerability in the wishnet Nepstech Wifi Router NTPL-XPON1GFEVN v1.0 allows an unauthenticated, remote attacker to obtain sensitive information via the manipulation of cookies. The issue arises due to insufficient security measures for cookies, leading to potential leakage of sensitive information and unauthorized access.

Details: The wishnet Nepstech Wifi Router NTPL-XPON1GFEVN v1.0 does not properly secure cookies, allowing sensitive information, such as session identifiers, to be accessed or manipulated by an attacker. This vulnerability can be exploited by an attacker who intercepts or forges cookies to gain unauthorized access to the router's management interface, potentially leading to further exploitation of the device.

Impact: Successful exploitation of this vulnerability could allow an attacker to gain unauthorized access to the router's management interface by leveraging insecure cookies, leading to potential control over the device and exposure of sensitive information.

Affected Versions: wishnet Nepstech Wifi Router NTPL-XPON1GFEVN v1.0

Remediation: Users are advised to upgrade to a firmware version that implements secure cookie handling practices, such as using the HttpOnly and Secure flags and ensuring that cookies are transmitted over HTTPS connections.
