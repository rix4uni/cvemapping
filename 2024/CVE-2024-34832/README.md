# CubeCart - Directory Traversal May Lead To RCE (CVE-2024-34832)

## TL;DR

In the admin panel, parameters such as `_g` and `node` are used to construct the path to include `.inc.php` files and execute PHP code. A malicious user with the ability to upload `.inc.php` files anywhere on the server can exploit a path traversal vulnerability to include them and execute malicious code.

## Prerequisites

- Access to the admin panel (any privileges should work, including no privileges at all);
- Ability to upload files containing the `.inc.php` extension anywhere in the server (e.g. access to FTP, another application on the same server that would allow file upload, new vulnerabilities in CubeCart’s upload features, etc).

## Exploitation

Let’s say there’s an FTP server running on the same server CubeCart is installed and a user is able to upload files to a specific location. In our case, let’s say anything that gets uploaded via FTP will end up in `/opt/FTP_Example`.

Let’s also say that this user uploaded a file called `path_traversal.inc.php` via FTP and its contents are the following PHP code `<?php system('whoami;id;hostname;ls') ?>`.

![image](https://github.com/julio-cfa/CVE-2024-34832/assets/52619625/a5058ea8-64e1-4a8d-b621-78d5e5751314)

Initially there is no danger in uploading such a file as it will not be executed nor it is in the directory of a web server - such as Apache - that could execute it.

This same user may have very limited or even no privileges at all on CubeCart’s admin panel, but they can still log into it. For example, we created a user called `julio` that has no privileges whatsoever.

![image](https://github.com/julio-cfa/CVE-2024-34832/assets/52619625/9487555e-4c9a-45a0-8dfb-4fecf488ea76)

After logging into the application as `julio`, we started testing the `_g` and `node` parameters. We noticed that these parameters would append `.inc.php` automatically to the end of a path and seemed to use `include()` on that file to execute PHP code.

As seen below, when the file isn’t found, the following error message is returned.

![image](https://github.com/julio-cfa/CVE-2024-34832/assets/52619625/32a818fb-0755-479c-8d7f-7f879644742a)

We started wondering if we could traverse the path and reach an `.inc.php` file in a directory somewhere else in the server - like our FTP folder. 

Since we had a file called `path_traversal.inc.php` in the `/opt/FTP_Example` folder, we tried adding lots of `/../../../` until we reached the root directory, we then added `/opt/FTP_Example/path_traversal` and the application automatically added `.inc.php` to the end of the path.

As seen below, code was successfully executed.

![image](https://github.com/julio-cfa/CVE-2024-34832/assets/52619625/e2ad1137-9f3c-4de5-a67e-99ffcd99422c)

## Conclusion

We noticed that the `node` parameter actually escapes slashes (`/`), but `_g` does not. All parameters used to construct paths should escape slashes to prevent path traversal vulnerabilities.

Although there are prerequisites for the successful exploitation of this vulnerability - which considerably reduces the risk - it still benefits from a patch. You can check in the references how the authors of CubeCart fixed this vulnerability and apply the fixes to your own instance of CubeCart until an official release comes with it already patched.

## References

- https://github.com/cubecart/v6/issues/3586
