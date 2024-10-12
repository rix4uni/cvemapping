# CVE-2024-42657
CVE-2024-42657 An issue in wishnet Nepstech Wifi Router NTPL-XPON1GFEVN v1.0 allows a remote attacker to obtain sensitive information via the lack of encryption during login process.


CVE-2024-42657:

Summary: A vulnerability in the wishnet Nepstech Wifi Router NTPL-XPON1GFEVN v1.0 allows an unauthenticated, remote attacker to obtain sensitive information during the login process. The issue arises due to the lack of encryption when transmitting login credentials, making it susceptible to interception via man-in-the-middle (MITM) attacks.

Details: The wishnet Nepstech Wifi Router NTPL-XPON1GFEVN v1.0 transmits sensitive information, including login credentials, over an unencrypted HTTP connection during the login process. This lack of encryption allows attackers who can intercept the traffic to capture and exploit the credentials. This vulnerability can lead to unauthorized access to the router's management interface and potential further exploitation of the device.

Impact: Successful exploitation of this vulnerability allows an attacker to capture sensitive information, including user credentials, potentially leading to unauthorized access and control over the router.

Affected Versions: wishnet Nepstech Wifi Router NTPL-XPON1GFEVN v1.0

Remediation: Users are advised to upgrade to a firmware version that enforces HTTPS encryption during the login process. Alternatively, users should consider deploying network-level encryption (such as VPNs) to secure their communications
