# CVE-2023-47504 POC

Exploit for CVE-2023-47504.
According to NIST, this vulnerability should allow unauthenticated users to access functionalities in the Elementor Website Builder Plugin.
Based on my research into the vulnerability, and also judging by the URL from Patchstack that describes the vulnerability: `https://patchstack.com/database/vulnerability/elementor/wordpress-elementor-plugin-3-16-4-contributor-arbitrary-attachment-read-vulnerability?_s_id=cve`, I recon this is actually requires credentials for at least a subscriber account.
Also, for the exploit to work one needs access to the `wp-config.php` file of the target website. 

## Requirements

1. Credentials for at least a subscriber account
2. Access to `wp-config.php`
3. Authorization to exploit the website ;)

## Usage

1. Proxy your traffic to burp, or use the browser's developers tool to intercept requests;
1. Go to `wp-admin/profile.php` and update your profile;
1. Get the `wordpress_logged_in_*` cookie and your user id from the request;
1. The required salt is the NONCE\_KEY + NONCE\_SALT string from `wp-config.php`
1. `python exploit.py --target <TARGET> --wordpress-cookie <COPIED COOKIE> --uid <COPIED USER ID> --salt <COPIED SALT>`;
1. If the target is vulnerable the elementor cache of the website will be deleted (files under `/wp-content/uploads/elementor/css`);

