# HeimShell (CVE-2023-51803)

**HeimShell** is an exploit for CVE-2023-51803, leveraging an arbitrary file-upload vulnerability in LinuxServer.io Heimdall (≤ 2.5.6). It will auto-detect the target version and either  warn of exploitability or remote fetch a php shell defined by `SHELL_URL` 

- **≤ 2.2.2**: Aribtrary file upload is possible but files are served statically and URLs are not remotely fetched
- **≥ 2.2.3 & ≤ 2.5.6**: remote-fetch PHP shell via icon URL upload  


---

* **Version Check:** Retrieves `/settings` and parses the Version field to ensure arbitrary upload capability exists.
* **CSRF Token Retrieval:** Loads `/items/create` and scrapes the hidden `_token` input.
* **Shell Deployment:** For versions ≥ 2.2.3, it uses the icon parameter pointing to a remote PHP shell URL on a webserver
* **Item Enumeration:** Scrapes the item list (`/items`) to find the dashboard entry matching the random tag.
* **Shell URL Extraction:** Checks edit page (`/items/<id>/edit`), finds `icon` or `#appimage img` element, and prints shell URL.

```
python heimShell.py <base_url>
detected version: 2.4.13
☠  shell uploaded at: <base_url>/storage/icons/abc123DEF456.php
```

## References
[https://nvd.nist.gov/vuln/detail/CVE-2023-51803](https://nvd.nist.gov/vuln/detail/CVE-2023-51803)

[https://rz.my/2024/06/cve-2023-51803-arbitrary-file-upload-in-linuxserverio-heimdall.html](https://rz.my/2024/06/cve-2023-51803-arbitrary-file-upload-in-linuxserverio-heimdall.html)



## Disclaimer

This tool is for authorized security testing only. Unauthorized use against systems you do not own or have explicit permission to test is illegal and unethical.
