# CVE-2024-5736
AdmirorFrames Joomla! Extension < 5.0 - Server-Side Request Forgery

## Timeline
- Vulnerability reported to vendor: 26.01.2024
- New fixed 5.0 version released: 06.06.2024
- Public disclosure: 28.06.2024

## Description

Server-Side Request Forgery in AdmirorFrames Joomla! Extension in `afGdStream.php` file which uses value of `$_GET['src_file']` variable directly as a parameter to `imagecreatefrompng` function. 

The vulnerability exists in `afGdStream.php` file:
```
if ($_GET['src_file'] == "")
    exit;

    $src_file = urldecode($_GET['src_file']);
    $bgcolor = $_GET['bgcolor'];
    $colorize = $_GET['colorize'];
    $ratio = $_GET['ratio'];

    // Create src_img
    if (preg_match("/png/i", $src_file))
    {
        @$src_img = imagecreatefrompng($src_file);
    }
```

This issue was caused by direct usage of `$_GET['src_file']` variable as a parameter to `imagecreatefrompng` function. This problem has been fixed in AdmirorFrames Joomla! Extension at version 5.0.

## Affected versions
< 5.0 

## Advisory
Update AdmirorFrames Joomla! Extension to version 5.0 or newer.

### References
* https://github.com/vasiljevski/admirorframes/issues/3
* https://cert.pl/en/posts/2024/06/CVE-2024-5735/
* https://cert.pl/posts/2024/06/CVE-2024-5735/
* https://nvd.nist.gov/vuln/detail/CVE-2024-5736
