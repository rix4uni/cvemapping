# CVE-2021-22873 - Revive Adserver Open Redirect Vulnerability

Revive Adserver before version 5.1.0 is vulnerable to open redirects via the dest, oadest, and/or ct0 parameters of the lg.php and ck.php delivery scripts. Originally, this functionality was designed to allow third-party ad servers to track metrics when delivering ads. However, due to security concerns, third-party click tracking via redirects is no longer considered a viable option, leading to the removal of this feature and its reclassification as a security vulnerability.

# Impact

The open redirect vulnerability in Revive Adserver could allow attackers to craft malicious URLs that redirect users to arbitrary websites. This could potentially be abused for phishing attacks, distributing malware, or tricking users into visiting malicious websites.

# PoC Exploit

GET /lg.php?dest=https://malicious-website.com HTTP/1.1
Host: example.com

# Steps to Reproduce

    Deploy Revive Adserver version before 5.1.0.
    Craft a malicious URL with the dest, oadest, or ct0 parameters pointing to a malicious website.
    Deliver the malicious URL as part of an ad.
    When a user clicks on the ad, they will be redirected to the malicious website.

# Disclaimer

This proof of concept is for educational purposes only. Use it responsibly and only on systems you have permission to test. The author is not responsible for any misuse or damage caused.
