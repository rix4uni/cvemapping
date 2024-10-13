# CVE-2019-19634 - class.upload.php <= 2.0.4 Arbitrary file upload
- Author - Jinny Ramsmark
- Affected vendor - Verot.net
- Affected product - class.upload.php <= 2.0.4
- Tested on newly installed Ubuntu 14.04 with PHP5 and Apache
- Specifically Debian/Ubuntu has been found to be vulnerable since they add the pht extension among others to available PHP handlers. In this case class.upload.php has not blacklisted the pht extension.
- This CVE is directly related to [CVE-2019-19576](https://github.com/jra89/CVE-2019-19576)

# Description
This is a filter bypass exploit that results in arbitrary file upload and remote code execution.
The class.upload.php script filters "dangerous files and content" and renames them to the txt file extension.
It also does different type of transformation on the uploaded image, which would normally destroy any injected payload, even if the file extension filter could be bypassed.

The file extension filter is a blacklist, so any time a new extension is introduced (in this case pht), or any has been missed, a PHP file can be uploaded.
The content must still be a valid image however and will still go through the imagecreatefromjpeg and similar functions.
For this purpose I wrote the inject.php script which will essentially bruteforce its way through different images until it finds one where the payload will not be destroyed by the process done in class.upload.php. This effectively gives us an arbitrary file upload and a very stealthy code execution since it's still a valid image and will be displayed like one on pages where uploaded.

The inject.php script will be rewritten soon to be a more general tool for this type of attack, but for now it will just be included as individual scripts in this type of CVE release.

# Timeline (90 day default deadline)
- 2019-12-07 - Reported to developer and K2 from JoomlaWorks (they are affected)
- 2019-12-07 - Developer responded and has released a patch
- 2019-12-08 - Developer has responded and agreed to release information

# Files included in this PoC
- composer.json
- upload.php
- inject.php

# Usage
The upload.php script is the example code from verot.net's github.
I thought it would be best to demonstrate this vulnerability using their own example code.

- Run "php inject.php" in a terminal, it will generate a sample image with a simple payload in the file.
- When the script is finished it will produce a file called "image.jpg.pht".
- Browse to the upload.php file and upload image.jpg.pht, it will go through and you will now have a shell

# Example
```
user@ayu:/var/www/html# php inject.php 
-=Imagejpeg injector 1.8=-
[+] Fetching image (100 X 100) from http://lorempixel.com/100/100/
[+] Jumping to end byte
[+] Searching for valid injection point
[!] Temp solution, if you get a 'recoverable parse error' here, it means it probably failed
[+] It seems like it worked!
[+] Result file: image.jpg.pht
```

```
user@ayu:/var/www/html# curl -v -o - http://localhost/images/image_resized.phar?c=uname%20-a | grep -aPo "(Linux.*GNU)"
Linux ayu 5.0.0-36-generic #39-Ubuntu SMP Tue Nov 12 09:46:06 UTC 2019 x86_64 x86_64 x86_64 GNU
```

# Proposed solution
- Don't blacklist file extensions.
- Use a whitelist of allowed ones by default instead.
- Or just don't have any extensions at all on uploaded files, and store the original name elsewhere.

# Reference
- https://github.com/verot/class.upload.php/blob/2.0.5/src/class.upload.php#L3068
