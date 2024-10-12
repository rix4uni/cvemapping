# CVE-2023-47129 - Statamic CMS versions <4.33.0 - Remote Code Execution

## Description
In versions <4.33.0 of Statamic CMS where the front-end has a form with active file upload, it is possible to send PHP files created to look like images, regardless of the mime validation rules. This vulnerability allows an attacker to upload arbitrary and potentially dangerous files and even execute server-side scripts.

## To Fix
Update Statamic CMS to version 4.33.0.

## Steps to Reproduce:

**1)** In a Statamic CMS installation, create a form and its respective page.

**2)** In the form blueprint, include an `Asset Field` and in the _“Validation”_ option select, for example, `mimetypes:image/jpeg`, `mimes:jpg`, `image`.

**3)** Create a polyglot jpg file with some php script, example: 

```exiftool -Comment="<?php phpinfo(); ?>" image.jpg```

**4)** Rename this file to `image.php`.

**5)** On the form page, upload the created `image.php` file.

**6)** Now, to run this file just access `https://yoursite.com/assets/image.php`

_Note: replace `https://yoursite.com` with the address of your test installation._

### Reference
* [GHSA-72hg-5wr5-rmfc](https://github.com/statamic/cms/security/advisories/GHSA-72hg-5wr5-rmfc)
