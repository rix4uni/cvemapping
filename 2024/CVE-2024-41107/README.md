<div align="center">

 #  🇮🇱  **#BringThemHome #NeverAgainIsNow**   🇮🇱

**We demand the safe return of all citizens who have been taken hostage by the terrorist group Hamas. We will not rest until every hostage is released and returns home safely. You can help bring them back home.
https://stories.bringthemhomenow.net/**

</div>
## 🚀 CVE-2024-41107 Exploit 🚀

This repository contains an exploit for the critical vulnerability identified as **CVE-2024-41107** in Apache CloudStack. This vulnerability affects versions **4.5.0 through 4.18.2.1** and **4.19.0.0 through 4.19.0.2**. The flaw lies within the Security Assertion Markup Language (SAML) authentication mechanism, allowing attackers to submit unsigned SAML responses to gain unauthorized access to user accounts and control over cloud resources.

## ⚠️ Disclaimer ⚠️

This code is for **educational purposes only**. Unauthorized access to computer systems is illegal and unethical. Use this information responsibly and within the boundaries of the law.

## ✨ Features ✨

- Exploits the SAML authentication vulnerability in Apache CloudStack
- Bypasses signature checks to gain unauthorized access
- Demonstrates the critical nature of CVE-2024-41107

## 🛠️ Requirements 🛠️

- Python 3.x
- `requests` library
- `beautifulsoup4` library

Install the required libraries using:

```bash
pip install requests beautifulsoup4
```

## 📄 Usage 📄

1. **Clone the repository:**

```bash
git clone https://github.com/d0rb/CVE-2024-41107/PoC.git
cd cve-2024-41107-exploit
```

2. **Edit the Exploit Code:**

Update the `url` and `saml_response_template` variables in `exploit.py` with the target CloudStack instance and your SAML issuer details.

3. **Run the Exploit:**

```bash
python exploit.py
```

4. **Check the Response:**

If successful, the script will print the session ID indicating unauthorized access.


## 🔒 Mitigation 🔒

To mitigate this vulnerability, users are advised to:

- Disable SAML authentication by setting the `saml2.enabled` global setting to `false`.
- Upgrade to the patched versions **4.18.2.2** or **4.19.1.0** released by Apache.
- Review access logs for signs of exploitation.



---

⚠️ **Disclaimer:** This code is for educational purposes only. Unauthorized use of this code is illegal. Always ensure you have permission before testing against any system.
